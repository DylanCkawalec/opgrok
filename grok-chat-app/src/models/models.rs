use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[cfg(feature = "server")]
use sqlx::FromRow;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatSession {
    pub id: String,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub model: String,
    pub title: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Message {
    pub id: i64,
    pub session_id: String,
    pub role: MessageRole,
    pub content: String,
    pub timestamp: DateTime<Utc>,
    pub model: Option<String>,
    pub tokens_used: Option<i32>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum MessageRole {
    #[serde(rename = "user")]
    User,
    #[serde(rename = "assistant")]
    Assistant,
    #[serde(rename = "system")]
    System,
}

impl std::fmt::Display for MessageRole {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            MessageRole::User => write!(f, "user"),
            MessageRole::Assistant => write!(f, "assistant"),
            MessageRole::System => write!(f, "system"),
        }
    }
}

impl From<String> for MessageRole {
    fn from(s: String) -> Self {
        match s.as_str() {
            "user" => MessageRole::User,
            "assistant" => MessageRole::Assistant,
            "system" => MessageRole::System,
            _ => MessageRole::User, // Default fallback
        }
    }
}

impl From<&str> for MessageRole {
    fn from(s: &str) -> Self {
        match s {
            "user" => MessageRole::User,
            "assistant" => MessageRole::Assistant,
            "system" => MessageRole::System,
            _ => MessageRole::User, // Default fallback
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ChatRequest {
    pub message: String,
    pub model: String,
    pub session_id: Option<String>,
    pub system_prompt: Option<String>,
    pub max_tokens: Option<i32>,
    pub temperature: Option<f32>,
    pub stream: Option<bool>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ChatResponse {
    pub session_id: String,
    pub message: Message,
    pub usage: Option<UsageStats>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct UsageStats {
    pub prompt_tokens: i32,
    pub completion_tokens: i32,
    pub total_tokens: i32,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ApiMessage {
    pub role: String,
    pub content: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ApiChatRequest {
    pub messages: Vec<ApiMessage>,
    pub model: String,
    pub max_tokens: Option<i32>,
    pub temperature: Option<f32>,
    pub stream: Option<bool>,
    pub system_prompt: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ApiChatResponse {
    pub id: String,
    pub object: String,
    pub created: i64,
    pub model: String,
    pub choices: Vec<Choice>,
    pub usage: Option<UsageStats>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Choice {
    pub index: i32,
    pub message: Option<ApiMessage>,
    pub delta: Option<Delta>,
    pub finish_reason: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Delta {
    pub role: Option<String>,
    pub content: Option<String>,
}

impl ChatSession {
    pub fn new(model: String, title: Option<String>) -> Self {
        let now = Utc::now();
        Self {
            id: Uuid::new_v4().to_string(),
            created_at: now,
            updated_at: now,
            model,
            title,
        }
    }

    pub fn update_timestamp(&mut self) {
        self.updated_at = Utc::now();
    }
}

impl Message {
    pub fn new(
        session_id: String,
        role: MessageRole,
        content: String,
        model: Option<String>,
    ) -> Self {
        Self {
            id: 0, // Will be set by database
            session_id,
            role,
            content,
            timestamp: Utc::now(),
            model,
            tokens_used: None,
        }
    }

    pub fn user(session_id: String, content: String) -> Self {
        Self::new(session_id, MessageRole::User, content, None)
    }

    pub fn assistant(session_id: String, content: String, model: Option<String>) -> Self {
        Self::new(session_id, MessageRole::Assistant, content, model)
    }

    pub fn system(session_id: String, content: String) -> Self {
        Self::new(session_id, MessageRole::System, content, None)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_message_role_display() {
        assert_eq!(MessageRole::User.to_string(), "user");
        assert_eq!(MessageRole::Assistant.to_string(), "assistant");
        assert_eq!(MessageRole::System.to_string(), "system");
    }

    #[test]
    fn test_message_role_from_string() {
        assert_eq!(MessageRole::from("user"), MessageRole::User);
        assert_eq!(MessageRole::from("assistant"), MessageRole::Assistant);
        assert_eq!(MessageRole::from("system"), MessageRole::System);
        assert_eq!(MessageRole::from("unknown"), MessageRole::User); // Default fallback
    }

    #[test]
    fn test_chat_session_creation() {
        let session = ChatSession::new("grok-4-0709".to_string(), Some("Test Chat".to_string()));
        assert!(!session.id.is_empty());
        assert_eq!(session.model, "grok-4-0709");
        assert_eq!(session.title, Some("Test Chat".to_string()));
    }

    #[test]
    fn test_message_creation() {
        let message = Message::user("session-123".to_string(), "Hello, world!".to_string());
        assert_eq!(message.session_id, "session-123");
        assert_eq!(message.role, MessageRole::User);
        assert_eq!(message.content, "Hello, world!");
        assert!(message.timestamp <= Utc::now());
    }

    #[test]
    fn test_api_message_serialization() {
        let api_message = ApiMessage {
            role: "user".to_string(),
            content: "Hello".to_string(),
        };

        let json = serde_json::to_string(&api_message).unwrap();
        assert!(json.contains("user"));
        assert!(json.contains("Hello"));
    }
}
