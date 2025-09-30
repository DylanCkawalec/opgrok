use anyhow::{anyhow, Result};
use futures_util::StreamExt;
use reqwest::{Client as HttpClient, Response};
use serde_json::{json, Value};
use std::collections::HashMap;
use tokio_stream::Stream;

use crate::config::Config;
use crate::models::{ApiChatRequest, ApiChatResponse, ApiMessage, Choice, Delta, UsageStats};

const XAI_API_BASE_URL: &str = "https://api.x.ai/v1";

pub struct XaiClient {
    client: HttpClient,
    api_key: String,
}

impl XaiClient {
    pub fn new(config: &Config) -> Self {
        let client = HttpClient::new();
        Self {
            client,
            api_key: config.xai_api_key().to_string(),
        }
    }

    pub async fn list_models(&self) -> Result<Vec<String>> {
        let response = self
            .client
            .get(&format!("{}/models", XAI_API_BASE_URL))
            .header("Authorization", format!("Bearer {}", self.api_key))
            .header("Content-Type", "application/json")
            .send()
            .await?;

        if !response.status().is_success() {
            return Err(anyhow!("Failed to list models: {}", response.status()));
        }

        let models_response: Value = response.json().await?;
        let models = models_response["data"]
            .as_array()
            .ok_or_else(|| anyhow!("Invalid response format for models"))?;

        let model_names: Vec<String> = models
            .iter()
            .filter_map(|model| {
                let id = model["id"].as_str()?;
                // Filter to text-based Grok models only
                if id.contains("grok") && !id.contains("vision") && !id.contains("image") {
                    Some(id.to_string())
                } else {
                    None
                }
            })
            .collect();

        Ok(model_names)
    }

    pub async fn chat_completion(
        &self,
        request: ApiChatRequest,
    ) -> Result<ApiChatResponse> {
        let mut request_body = json!({
            "model": request.model,
            "messages": request.messages,
            "stream": request.stream.unwrap_or(false),
        });

        if let Some(max_tokens) = request.max_tokens {
            request_body["max_tokens"] = json!(max_tokens);
        }

        if let Some(temperature) = request.temperature {
            request_body["temperature"] = json!(temperature);
        }

        if let Some(system_prompt) = request.system_prompt {
            // Add system message to the beginning of messages
            let messages_array = request_body["messages"].as_array_mut().unwrap();
            messages_array.insert(
                0,
                json!({
                    "role": "system",
                    "content": system_prompt
                }),
            );
        }

        let response = self
            .client
            .post(&format!("{}/chat/completions", XAI_API_BASE_URL))
            .header("Authorization", format!("Bearer {}", self.api_key))
            .header("Content-Type", "application/json")
            .json(&request_body)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_text = response.text().await.unwrap_or_default();
            return Err(anyhow!(
                "API request failed with status {}: {}",
                response.status(),
                error_text
            ));
        }

        let chat_response: ApiChatResponse = response.json().await?;
        Ok(chat_response)
    }

    pub async fn chat_completion_stream(
        &self,
        request: ApiChatRequest,
    ) -> Result<impl Stream<Item = Result<String>>> {
        let mut request_body = json!({
            "model": request.model,
            "messages": request.messages,
            "stream": true,
        });

        if let Some(max_tokens) = request.max_tokens {
            request_body["max_tokens"] = json!(max_tokens);
        }

        if let Some(temperature) = request.temperature {
            request_body["temperature"] = json!(temperature);
        }

        if let Some(system_prompt) = request.system_prompt {
            let messages_array = request_body["messages"].as_array_mut().unwrap();
            messages_array.insert(
                0,
                json!({
                    "role": "system",
                    "content": system_prompt
                }),
            );
        }

        let response = self
            .client
            .post(&format!("{}/chat/completions", XAI_API_BASE_URL))
            .header("Authorization", format!("Bearer {}", self.api_key))
            .header("Content-Type", "application/json")
            .json(&request_body)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_text = response.text().await.unwrap_or_default();
            return Err(anyhow!(
                "API request failed with status {}: {}",
                response.status(),
                error_text
            ));
        }

        let stream = response.bytes_stream();
        let content_stream = stream.filter_map(move |chunk| {
            let chunk = chunk.ok()?;
            let text = String::from_utf8_lossy(&chunk);

            // Parse SSE-like stream format
            let lines: Vec<&str> = text.split('\n').collect();
            let mut content = String::new();

            for line in lines {
                if line.starts_with("data: ") {
                    let data = &line[6..]; // Remove "data: " prefix
                    if data == "[DONE]" {
                        continue;
                    }

                    if let Ok(chunk_data) = serde_json::from_str::<Value>(data) {
                        if let Some(choices) = chunk_data["choices"].as_array() {
                            for choice in choices {
                                if let Some(delta) = choice["delta"].as_object() {
                                    if let Some(delta_content) = delta["content"].as_str() {
                                        content.push_str(delta_content);
                                    }
                                }
                            }
                        }
                    }
                }
            }

            if content.is_empty() {
                None
            } else {
                Some(Ok(content))
            }
        });

        Ok(content_stream)
    }

    pub async fn validate_api_key(&self) -> Result<bool> {
        match self.list_models().await {
            Ok(_) => Ok(true),
            Err(_) => Ok(false),
        }
    }
}

pub struct ChatService {
    client: XaiClient,
    default_system_prompt: String,
}

impl ChatService {
    pub fn new(config: &Config) -> Self {
        Self {
            client: XaiClient::new(config),
            default_system_prompt: "You are Grok, a helpful and maximally truthful AI built by xAI, not based on any other companies and their models.".to_string(),
        }
    }

    pub async fn send_message(
        &self,
        messages: Vec<ApiMessage>,
        model: String,
        max_tokens: Option<i32>,
        temperature: Option<f32>,
        stream: bool,
    ) -> Result<ChatResponse> {
        let request = ApiChatRequest {
            messages,
            model,
            max_tokens,
            temperature,
            stream: Some(stream),
            system_prompt: Some(self.default_system_prompt.clone()),
        };

        if stream {
            let content_stream = self.client.chat_completion_stream(request).await?;
            Ok(ChatResponse::Stream(content_stream))
        } else {
            let response = self.client.chat_completion(request).await?;
            Ok(ChatResponse::Complete(response))
        }
    }

    pub async fn list_available_models(&self) -> Result<Vec<String>> {
        self.client.list_models().await
    }
}

pub enum ChatResponse {
    Complete(ApiChatResponse),
    Stream(impl Stream<Item = Result<String>>),
}

impl ApiChatResponse {
    pub fn get_content(&self) -> Result<String> {
        let choices = &self.choices;
        if choices.is_empty() {
            return Err(anyhow!("No choices in response"));
        }

        let first_choice = &choices[0];
        if let Some(message) = &first_choice.message {
            Ok(message.content.clone())
        } else {
            Err(anyhow!("No message in first choice"))
        }
    }

    pub fn get_usage(&self) -> Option<&UsageStats> {
        self.usage.as_ref()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::config::Config;

    #[tokio::test]
    async fn test_xai_client_creation() {
        let config = Config {
            xai_api_key: "test-key".to_string(),
            database_url: "sqlite:test.db".to_string(),
            server_host: "127.0.0.1".to_string(),
            server_port: 3000,
            default_model: "grok-4-0709".to_string(),
        };

        let client = XaiClient::new(&config);
        assert_eq!(client.api_key, "test-key");
    }

    #[test]
    fn test_api_message_creation() {
        let message = ApiMessage {
            role: "user".to_string(),
            content: "Hello, world!".to_string(),
        };

        let json = serde_json::to_string(&message).unwrap();
        assert!(json.contains("user"));
        assert!(json.contains("Hello, world!"));
    }

    #[test]
    fn test_api_chat_request_creation() {
        let messages = vec![
            ApiMessage {
                role: "system".to_string(),
                content: "You are helpful".to_string(),
            },
            ApiMessage {
                role: "user".to_string(),
                content: "Hello".to_string(),
            },
        ];

        let request = ApiChatRequest {
            messages,
            model: "grok-4-0709".to_string(),
            max_tokens: Some(100),
            temperature: Some(0.7),
            stream: Some(false),
            system_prompt: Some("Custom prompt".to_string()),
        };

        let json = serde_json::to_string(&request).unwrap();
        assert!(json.contains("grok-4-0709"));
        assert!(json.contains("Hello"));
        assert!(json.contains("Custom prompt"));
    }
}
