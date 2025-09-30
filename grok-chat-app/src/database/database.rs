use anyhow::{anyhow, Result};
use chrono::{DateTime, Utc};
use sqlx::SqlitePool;

use crate::config::Config;
use crate::models::{ChatSession, Message, MessageRole};

pub struct Database {
    pool: SqlitePool,
}

impl Database {
    pub async fn new(config: &Config) -> Result<Self> {
        let pool = SqlitePool::connect(config.database_url()).await?;

        let db = Self { pool };
        db.init_tables().await?;
        Ok(db)
    }

    async fn init_tables(&self) -> Result<()> {
        // Create chat_sessions table
        sqlx::query(
            r#"
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                model TEXT NOT NULL,
                title TEXT
            )
            "#,
        )
        .execute(&self.pool)
        .await?;

        // Create messages table
        sqlx::query(
            r#"
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                model TEXT,
                tokens_used INTEGER,
                FOREIGN KEY (session_id) REFERENCES chat_sessions (id) ON DELETE CASCADE
            )
            "#,
        )
        .execute(&self.pool)
        .await?;

        // Create indexes for better performance
        sqlx::query(
            r#"
            CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id);
            CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
            CREATE INDEX IF NOT EXISTS idx_chat_sessions_created_at ON chat_sessions(created_at);
            "#,
        )
        .execute(&self.pool)
        .await?;

        Ok(())
    }

    pub async fn create_session(&self, mut session: ChatSession) -> Result<ChatSession> {
        session.update_timestamp();

        sqlx::query(
            r#"
            INSERT INTO chat_sessions (id, created_at, updated_at, model, title)
            VALUES (?, ?, ?, ?, ?)
            "#,
        )
        .bind(&session.id)
        .bind(session.created_at.to_rfc3339())
        .bind(session.updated_at.to_rfc3339())
        .bind(&session.model)
        .bind(&session.title)
        .execute(&self.pool)
        .await?;

        Ok(session)
    }

    pub async fn get_session(&self, session_id: &str) -> Result<Option<ChatSession>> {
        let row = sqlx::query(
            r#"
            SELECT id, created_at, updated_at, model, title
            FROM chat_sessions
            WHERE id = ?
            "#,
        )
        .bind(session_id)
        .fetch_optional(&self.pool)
        .await?;

        if let Some(row) = row {
            Ok(Some(ChatSession {
                id: row.get::<String, _>(0),
                created_at: DateTime::parse_from_rfc3339(&row.get::<String, _>(1))?
                    .with_timezone(&Utc),
                updated_at: DateTime::parse_from_rfc3339(&row.get::<String, _>(2))?
                    .with_timezone(&Utc),
                model: row.get::<String, _>(3),
                title: row.get::<Option<String>, _>(4),
            }))
        } else {
            Ok(None)
        }
    }

    pub async fn list_sessions(&self, limit: Option<i64>, offset: Option<i64>) -> Result<Vec<ChatSession>> {
        let limit = limit.unwrap_or(50);
        let offset = offset.unwrap_or(0);

        let rows = sqlx::query(
            r#"
            SELECT id, created_at, updated_at, model, title
            FROM chat_sessions
            ORDER BY updated_at DESC
            LIMIT ? OFFSET ?
            "#,
        )
        .bind(limit)
        .bind(offset)
        .fetch_all(&self.pool)
        .await?;

        let mut sessions = Vec::new();
        for row in rows {
            sessions.push(ChatSession {
                id: row.get::<String, _>(0),
                created_at: DateTime::parse_from_rfc3339(&row.get::<String, _>(1))?
                    .with_timezone(&Utc),
                updated_at: DateTime::parse_from_rfc3339(&row.get::<String, _>(2))?
                    .with_timezone(&Utc),
                model: row.get::<String, _>(3),
                title: row.get::<Option<String>, _>(4),
            });
        }

        Ok(sessions)
    }

    pub async fn update_session(&self, session_id: &str, title: Option<String>) -> Result<()> {
        let updated_at = Utc::now().to_rfc3339();

        if let Some(title) = title {
            sqlx::query(
                r#"
                UPDATE chat_sessions
                SET updated_at = ?, title = ?
                WHERE id = ?
                "#,
            )
            .bind(updated_at)
            .bind(title)
            .bind(session_id)
            .execute(&self.pool)
            .await?;
        } else {
            sqlx::query(
                r#"
                UPDATE chat_sessions
                SET updated_at = ?
                WHERE id = ?
                "#,
            )
            .bind(updated_at)
            .bind(session_id)
            .execute(&self.pool)
            .await?;
        }

        Ok(())
    }

    pub async fn delete_session(&self, session_id: &str) -> Result<()> {
        sqlx::query("DELETE FROM chat_sessions WHERE id = ?")
            .bind(session_id)
            .execute(&self.pool)
            .await?;

        Ok(())
    }

    pub async fn create_message(&self, mut message: Message) -> Result<Message> {
        let result = sqlx::query(
            r#"
            INSERT INTO messages (session_id, role, content, timestamp, model, tokens_used)
            VALUES (?, ?, ?, ?, ?, ?)
            "#,
        )
        .bind(&message.session_id)
        .bind(message.role.to_string())
        .bind(&message.content)
        .bind(message.timestamp.to_rfc3339())
        .bind(&message.model)
        .bind(message.tokens_used)
        .execute(&self.pool)
        .await?;

        message.id = result.last_insert_rowid();
        Ok(message)
    }

    pub async fn get_messages(&self, session_id: &str) -> Result<Vec<Message>> {
        let rows = sqlx::query(
            r#"
            SELECT id, session_id, role, content, timestamp, model, tokens_used
            FROM messages
            WHERE session_id = ?
            ORDER BY timestamp ASC
            "#,
        )
        .bind(session_id)
        .fetch_all(&self.pool)
        .await?;

        let mut messages = Vec::new();
        for row in rows {
            messages.push(Message {
                id: row.get::<i64, _>(0),
                session_id: row.get::<String, _>(1),
                role: MessageRole::from(row.get::<String, _>(2)),
                content: row.get::<String, _>(3),
                timestamp: DateTime::parse_from_rfc3339(&row.get::<String, _>(4))?
                    .with_timezone(&Utc),
                model: row.get::<Option<String>, _>(5),
                tokens_used: row.get::<Option<i32>, _>(6),
            });
        }

        Ok(messages)
    }

    pub async fn get_session_message_count(&self, session_id: &str) -> Result<i64> {
        let row = sqlx::query("SELECT COUNT(*) as count FROM messages WHERE session_id = ?")
            .bind(session_id)
            .fetch_one(&self.pool)
            .await?;

        Ok(row.get::<i64, _>("count"))
    }

    pub async fn get_total_sessions(&self) -> Result<i64> {
        let row = sqlx::query("SELECT COUNT(*) as count FROM chat_sessions")
            .fetch_one(&self.pool)
            .await?;

        Ok(row.get::<i64, _>("count"))
    }

    pub async fn get_total_messages(&self) -> Result<i64> {
        let row = sqlx::query("SELECT COUNT(*) as count FROM messages")
            .fetch_one(&self.pool)
            .await?;

        Ok(row.get::<i64, _>("count"))
    }
}

pub async fn init() -> Result<Database> {
    let config = crate::config::load_config()?;
    Database::new(&config).await
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;

    async fn setup_test_db() -> Database {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let database_url = format!("sqlite:{}", db_path.to_string_lossy());

        // Override config for testing
        std::env::set_var("DATABASE_URL", &database_url);

        let config = Config {
            xai_api_key: "test-key".to_string(),
            database_url,
            server_host: "127.0.0.1".to_string(),
            server_port: 3000,
            default_model: "grok-4-0709".to_string(),
        };

        Database::new(&config).await.unwrap()
    }

    #[tokio::test]
    async fn test_create_and_get_session() {
        let db = setup_test_db().await;

        let session = ChatSession::new("grok-4-0709".to_string(), Some("Test Session".to_string()));
        let created_session = db.create_session(session.clone()).await.unwrap();

        assert_eq!(created_session.id, session.id);
        assert_eq!(created_session.model, session.model);
        assert_eq!(created_session.title, session.title);

        let retrieved_session = db.get_session(&session.id).await.unwrap().unwrap();
        assert_eq!(retrieved_session.id, session.id);
        assert_eq!(retrieved_session.model, "grok-4-0709");
    }

    #[tokio::test]
    async fn test_create_and_get_messages() {
        let db = setup_test_db().await;

        let session = ChatSession::new("grok-4-0709".to_string(), None);
        db.create_session(session.clone()).await.unwrap();

        let user_message = Message::user(session.id.clone(), "Hello, Grok!".to_string());
        let assistant_message = Message::assistant(
            session.id.clone(),
            "Hello! How can I help you today?".to_string(),
            Some("grok-4-0709".to_string()),
        );

        db.create_message(user_message.clone()).await.unwrap();
        db.create_message(assistant_message.clone()).await.unwrap();

        let messages = db.get_messages(&session.id).await.unwrap();
        assert_eq!(messages.len(), 2);

        assert_eq!(messages[0].content, user_message.content);
        assert_eq!(messages[0].role, MessageRole::User);

        assert_eq!(messages[1].content, assistant_message.content);
        assert_eq!(messages[1].role, MessageRole::Assistant);
        assert_eq!(messages[1].model, Some("grok-4-0709".to_string()));
    }

    #[tokio::test]
    async fn test_session_message_count() {
        let db = setup_test_db().await;

        let session = ChatSession::new("grok-4-0709".to_string(), None);
        db.create_session(session.clone()).await.unwrap();

        let count = db.get_session_message_count(&session.id).await.unwrap();
        assert_eq!(count, 0);

        let message = Message::user(session.id.clone(), "Test message".to_string());
        db.create_message(message).await.unwrap();

        let count = db.get_session_message_count(&session.id).await.unwrap();
        assert_eq!(count, 1);
    }

    #[tokio::test]
    async fn test_list_sessions() {
        let db = setup_test_db().await;

        let session1 = ChatSession::new("grok-4-0709".to_string(), Some("Session 1".to_string()));
        let session2 = ChatSession::new("grok-3".to_string(), Some("Session 2".to_string()));

        db.create_session(session1.clone()).await.unwrap();
        db.create_session(session2.clone()).await.unwrap();

        let sessions = db.list_sessions(Some(10), Some(0)).await.unwrap();
        assert_eq!(sessions.len(), 2);

        // Should be ordered by updated_at desc
        assert_eq!(sessions[0].id, session2.id);
        assert_eq!(sessions[1].id, session1.id);
    }
}
