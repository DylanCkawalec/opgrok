use anyhow::Result;
use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    response::{Html, IntoResponse, Json},
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;
use uuid::Uuid;

use crate::client::{ChatResponse, ChatService};
use crate::config::Config;
use crate::database::Database;
use crate::models::{ApiMessage, ChatSession, Message, MessageRole};

#[derive(Clone)]
pub struct AppState {
    pub chat_service: ChatService,
    pub database: Database,
    pub sessions: Arc<RwLock<HashMap<String, Vec<Message>>>>,
}

#[derive(Deserialize)]
pub struct CreateSessionRequest {
    pub model: Option<String>,
    pub title: Option<String>,
}

#[derive(Deserialize)]
pub struct SendMessageRequest {
    pub message: String,
    pub model: Option<String>,
}

#[derive(Serialize)]
pub struct ApiResponse<T> {
    pub success: bool,
    pub data: Option<T>,
    pub error: Option<String>,
}

impl<T> ApiResponse<T> {
    pub fn success(data: T) -> Self {
        Self {
            success: true,
            data: Some(data),
            error: None,
        }
    }

    pub fn error(error: String) -> ApiResponse<()> {
        ApiResponse {
            success: false,
            data: None,
            error: Some(error),
        }
    }
}

pub async fn run_server(host: String, port: u16) -> Result<()> {
    let config = Config::from_env()?;
    let chat_service = ChatService::new(&config);
    let database = Database::new(&config).await?;

    let state = AppState {
        chat_service,
        database,
        sessions: Arc::new(RwLock::new(HashMap::new())),
    };

    let app = Router::new()
        .route("/", get(index_handler))
        .route("/health", get(health_handler))
        .route(
            "/sessions",
            get(list_sessions_handler).post(create_session_handler),
        )
        .route("/sessions/:session_id", get(get_session_handler))
        .route(
            "/sessions/:session_id/messages",
            get(get_messages_handler).post(send_message_handler),
        )
        .route("/models", get(list_models_handler));

    let app = app.with_state(state);

    let addr = format!("{}:{}", host, port);
    println!("🚀 Grok Chat API server starting on http://{}", addr);
    println!("📖 API Documentation:");
    println!("   GET  /health - Health check");
    println!("   GET  /sessions - List chat sessions");
    println!("   POST /sessions - Create new session");
    println!("   GET  /sessions/:id - Get session details");
    println!("   GET  /sessions/:id/messages - Get session messages");
    println!("   POST /sessions/:id/messages - Send message to session");
    println!("   GET  /models - List available models");
    println!();

    let listener = tokio::net::TcpListener::bind(&addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}

async fn index_handler() -> Html<&'static str> {
    Html(
        r#"<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grok Chat API</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #333; }
        .endpoint {
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #007acc;
            border-radius: 4px;
        }
        .method { font-weight: bold; color: #007acc; }
        code { background: #e9ecef; padding: 2px 6px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Grok Chat API</h1>
        <p>Welcome to the Grok Chat API! This is a local chat application that interfaces with xAI's Grok models.</p>

        <h2>Available Endpoints</h2>

        <div class="endpoint">
            <div class="method">GET /health</div>
            <p>Health check endpoint</p>
        </div>

        <div class="endpoint">
            <div class="method">GET /sessions</div>
            <p>List all chat sessions</p>
        </div>

        <div class="endpoint">
            <div class="method">POST /sessions</div>
            <p>Create a new chat session</p>
            <p><strong>Body:</strong> <code>{"model": "grok-4-0709", "title": "My Chat"}</code></p>
        </div>

        <div class="endpoint">
            <div class="method">GET /sessions/{session_id}</div>
            <p>Get details of a specific session</p>
        </div>

        <div class="endpoint">
            <div class="method">GET /sessions/{session_id}/messages</div>
            <p>Get all messages in a session</p>
        </div>

        <div class="endpoint">
            <div class="method">POST /sessions/{session_id}/messages</div>
            <p>Send a message to a session</p>
            <p><strong>Body:</strong> <code>{"message": "Hello, Grok!", "model": "grok-4-0709"}</code></p>
        </div>

        <div class="endpoint">
            <div class="method">GET /models</div>
            <p>List available Grok models</p>
        </div>

        <h2>Terminal Usage</h2>
        <p>Run the terminal interface with:</p>
        <code>cargo run --features terminal -- --terminal</code>

        <h2>Configuration</h2>
        <p>Set your xAI API key in the <code>XAI_API_KEY</code> environment variable.</p>
    </div>
</body>
</html>"#,
    )
}

async fn health_handler() -> impl IntoResponse {
    Json(ApiResponse::success("OK"))
}

async fn list_sessions_handler(State(state): State<AppState>) -> impl IntoResponse {
    match state.database.list_sessions(Some(50), Some(0)).await {
        Ok(sessions) => Json(ApiResponse::success(sessions)).into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ApiResponse::<()>::error(e.to_string())),
        )
            .into_response(),
    }
}

async fn create_session_handler(
    State(state): State<AppState>,
    Json(request): Json<CreateSessionRequest>,
) -> impl IntoResponse {
    let model = request.model.unwrap_or_else(|| "grok-4-0709".to_string());
    let session = ChatSession::new(model, request.title);

    match state.database.create_session(session.clone()).await {
        Ok(_) => Json(ApiResponse::success(session)).into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ApiResponse::<()>::error(e.to_string())),
        )
            .into_response(),
    }
}

async fn get_session_handler(
    State(state): State<AppState>,
    Path(session_id): Path<String>,
) -> impl IntoResponse {
    match state.database.get_session(&session_id).await {
        Ok(Some(session)) => Json(ApiResponse::success(session)).into_response(),
        Ok(None) => (
            StatusCode::NOT_FOUND,
            Json(ApiResponse::<()>::error("Session not found".to_string())),
        )
            .into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ApiResponse::<()>::error(e.to_string())),
        )
            .into_response(),
    }
}

async fn get_messages_handler(
    State(state): State<AppState>,
    Path(session_id): Path<String>,
) -> impl IntoResponse {
    match state.database.get_messages(&session_id).await {
        Ok(messages) => Json(ApiResponse::success(messages)).into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ApiResponse::<()>::error(e.to_string())),
        )
            .into_response(),
    }
}

async fn send_message_handler(
    State(state): State<AppState>,
    Path(session_id): Path<String>,
    Json(request): Json<SendMessageRequest>,
) -> impl IntoResponse {
    // Get existing messages for context
    let existing_messages = match state.database.get_messages(&session_id).await {
        Ok(msgs) => msgs,
        Err(e) => {
            return (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(ApiResponse::<()>::error(e.to_string())),
            )
                .into_response();
        }
    };

    // Convert to API messages
    let mut api_messages: Vec<ApiMessage> = existing_messages
        .into_iter()
        .map(|msg| ApiMessage {
            role: msg.role.to_string(),
            content: msg.content,
        })
        .collect();

    // Add the new user message
    api_messages.push(ApiMessage {
        role: "user".to_string(),
        content: request.message.clone(),
    });

    // Save user message to database
    let user_message = Message::user(session_id.clone(), request.message);
    if let Err(e) = state.database.create_message(user_message).await {
        return (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ApiResponse::<()>::error(e.to_string())),
        )
            .into_response();
    }

    // Send to Grok API
    let model = request.model.unwrap_or_else(|| "grok-4-0709".to_string());
    match state
        .chat_service
        .send_message(api_messages, model, Some(2048), Some(0.7), false)
        .await
    {
        Ok(ChatResponse::Complete(response)) => {
            let content = response
                .get_content()
                .unwrap_or_else(|_| "No response content".to_string());

            // Save assistant response to database
            let assistant_message =
                Message::assistant(session_id.clone(), content.clone(), Some(model));
            if let Err(e) = state.database.create_message(assistant_message).await {
                eprintln!("Failed to save assistant message: {}", e);
            }

            Json(ApiResponse::success(content)).into_response()
        }
        Ok(ChatResponse::Stream(_)) => (
            StatusCode::NOT_IMPLEMENTED,
            Json(ApiResponse::<()>::error(
                "Streaming not supported in this endpoint".to_string(),
            )),
        )
            .into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ApiResponse::<()>::error(e.to_string())),
        )
            .into_response(),
    }
}

async fn list_models_handler(State(state): State<AppState>) -> impl IntoResponse {
    match state.chat_service.list_available_models().await {
        Ok(models) => Json(ApiResponse::success(models)).into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ApiResponse::<()>::error(e.to_string())),
        )
            .into_response(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_api_response_success() {
        let response = ApiResponse::success("test data");
        assert!(response.success);
        assert_eq!(response.data, Some("test data"));
        assert_eq!(response.error, None);
    }

    #[test]
    fn test_api_response_error() {
        let response: ApiResponse<()> = ApiResponse::error("test error".to_string());
        assert!(!response.success);
        assert_eq!(response.data, None);
        assert_eq!(response.error, Some("test error".to_string()));
    }

    #[test]
    fn test_create_session_request() {
        let request = CreateSessionRequest {
            model: Some("grok-4-0709".to_string()),
            title: Some("Test Session".to_string()),
        };

        let json = serde_json::to_string(&request).unwrap();
        assert!(json.contains("grok-4-0709"));
        assert!(json.contains("Test Session"));
    }

    #[test]
    fn test_send_message_request() {
        let request = SendMessageRequest {
            message: "Hello, Grok!".to_string(),
            model: Some("grok-3".to_string()),
        };

        let json = serde_json::to_string(&request).unwrap();
        assert!(json.contains("Hello, Grok!"));
        assert!(json.contains("grok-3"));
    }
}
