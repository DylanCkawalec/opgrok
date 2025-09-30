use anyhow::{anyhow, Result};
use serde::{Deserialize, Serialize};
use std::env;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    pub xai_api_key: String,
    pub database_url: String,
    pub server_host: String,
    pub server_port: u16,
    pub default_model: String,
}

impl Config {
    pub fn from_env() -> Result<Self> {
        let xai_api_key = env::var("XAI_API_KEY")
            .map_err(|_| anyhow!("XAI_API_KEY environment variable is required"))?;

        let database_url =
            env::var("DATABASE_URL").unwrap_or_else(|_| "sqlite:grok_chat.db".to_string());

        let server_host = env::var("SERVER_HOST").unwrap_or_else(|_| "127.0.0.1".to_string());

        let server_port = env::var("SERVER_PORT")
            .unwrap_or_else(|_| "3000".to_string())
            .parse::<u16>()
            .map_err(|_| anyhow!("Invalid SERVER_PORT value"))?;

        let default_model = env::var("DEFAULT_MODEL").unwrap_or_else(|_| "grok-4-0709".to_string());

        Ok(Config {
            xai_api_key,
            database_url,
            server_host,
            server_port,
            default_model,
        })
    }

    pub fn xai_api_key(&self) -> &str {
        &self.xai_api_key
    }

    pub fn database_url(&self) -> &str {
        &self.database_url
    }

    pub fn server_host(&self) -> &str {
        &self.server_host
    }

    pub fn server_port(&self) -> u16 {
        self.server_port
    }

    pub fn default_model(&self) -> &str {
        &self.default_model
    }
}

impl Default for Config {
    fn default() -> Self {
        Self {
            xai_api_key: "".to_string(),
            database_url: "sqlite:grok_chat.db".to_string(),
            server_host: "127.0.0.1".to_string(),
            server_port: 3000,
            default_model: "grok-4-0709".to_string(),
        }
    }
}

pub fn load_config() -> Result<Config> {
    Config::from_env()
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::env;

    #[test]
    fn test_config_from_env() {
        env::set_var("XAI_API_KEY", "test-key");
        env::set_var("DATABASE_URL", "sqlite:test.db");
        env::set_var("SERVER_HOST", "localhost");
        env::set_var("SERVER_PORT", "8080");
        env::set_var("DEFAULT_MODEL", "grok-3");

        let config = Config::from_env().unwrap();
        assert_eq!(config.xai_api_key(), "test-key");
        assert_eq!(config.database_url(), "sqlite:test.db");
        assert_eq!(config.server_host(), "localhost");
        assert_eq!(config.server_port(), 8080);
        assert_eq!(config.default_model(), "grok-3");
    }

    #[test]
    fn test_config_defaults() {
        env::remove_var("XAI_API_KEY");
        env::remove_var("DATABASE_URL");
        env::remove_var("SERVER_HOST");
        env::remove_var("SERVER_PORT");
        env::remove_var("DEFAULT_MODEL");

        let config = Config::from_env().unwrap();
        assert_eq!(config.database_url(), "sqlite:grok_chat.db");
        assert_eq!(config.server_host(), "127.0.0.1");
        assert_eq!(config.server_port(), 3000);
        assert_eq!(config.default_model(), "grok-4-0709");
    }

    #[test]
    fn test_config_missing_api_key() {
        env::remove_var("XAI_API_KEY");

        let result = Config::from_env();
        assert!(result.is_err());
        assert!(result.unwrap_err().to_string().contains("XAI_API_KEY"));
    }
}
