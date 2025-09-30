use anyhow::Result;
use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use ratatui::{
    backend::CrosstermBackend,
    layout::{Constraint, Direction, Layout, Rect},
    style::{Color, Modifier, Style},
    text::{Line, Span},
    widgets::{Block, Borders, Clear, List, ListItem, Paragraph, Wrap},
    Frame,
};
use std::io::{self, Stdout};
use uuid::Uuid;

use crate::config::Config;
use crate::models::{ApiMessage, Message, MessageRole};

type AppTerminal = ratatui::Terminal<CrosstermBackend<Stdout>>;

pub struct ChatUI {
    terminal: AppTerminal,
    api_key: String,
    current_session_id: Option<String>,
    messages: Vec<Message>,
    input_buffer: String,
    input_mode: InputMode,
    available_models: Vec<String>,
    selected_model: String,
    status_message: String,
    show_help: bool,
    system_prompt: String,
    max_tokens: i32,
    temperature: f32,
}

#[derive(Debug, Clone, PartialEq)]
enum InputMode {
    Normal,
    Insert,
}

impl ChatUI {
    pub async fn new() -> Result<Self> {
        let config = Config::from_env()?;
        let api_key = config.xai_api_key().to_string();

        let terminal = setup_terminal()?;

        let available_models = vec![
            "grok-4-0709".to_string(),
            "grok-4-fast-reasoning".to_string(),
            "grok-4-fast-non-reasoning".to_string(),
            "grok-3".to_string(),
            "grok-3-mini".to_string(),
        ];

        let selected_model = config.default_model().to_string();
        let system_prompt = "You are Grok, a helpful and maximally truthful AI built by xAI, not based on any other companies and their models.".to_string();

        Ok(Self {
            terminal,
            api_key,
            current_session_id: None,
            messages: Vec::new(),
            input_buffer: String::new(),
            input_mode: InputMode::Insert,
            available_models,
            selected_model,
            status_message: "Ready to chat! Type your message and press Enter to send.".to_string(),
            show_help: false,
            system_prompt,
            max_tokens: 2048,
            temperature: 0.7,
        })
    }

    pub async fn run(&mut self) -> Result<()> {
        self.render()?;

        loop {
            if crossterm::event::poll(std::time::Duration::from_millis(100))? {
                if let Event::Key(key) = event::read()? {
                    match self.input_mode {
                        InputMode::Insert => match key.code {
                            KeyCode::Enter => {
                                if !self.input_buffer.trim().is_empty() {
                                    self.send_message().await?;
                                }
                            }
                            KeyCode::Esc => {
                                self.input_mode = InputMode::Normal;
                                self.status_message =
                                    "Press 'i' to insert, 'h' for help, 'q' to quit".to_string();
                            }
                            KeyCode::Backspace => {
                                self.input_buffer.pop();
                            }
                            KeyCode::Char(c) => {
                                self.input_buffer.push(c);
                            }
                            KeyCode::Up => {
                                // Navigate message history (simplified)
                            }
                            KeyCode::Down => {
                                // Navigate message history (simplified)
                            }
                            _ => {}
                        },
                        InputMode::Normal => match key.code {
                            KeyCode::Char('q') => break,
                            KeyCode::Char('i') => {
                                self.input_mode = InputMode::Insert;
                                self.status_message =
                                    "Insert mode: Type your message and press Enter".to_string();
                            }
                            KeyCode::Char('h') => {
                                self.show_help = !self.show_help;
                            }
                            KeyCode::Char('c') => {
                                self.create_new_session().await?;
                            }
                            KeyCode::Char('m') => {
                                self.cycle_model();
                            }
                            KeyCode::Char('l') => {
                                self.load_session_list()?;
                            }
                            _ => {}
                        },
                    }
                }
                self.render()?;
            }
        }

        Ok(())
    }

    async fn send_message(&mut self) -> Result<()> {
        let user_message = self.input_buffer.clone();
        self.input_buffer.clear();

        // Add user message to UI immediately
        let session_id = self
            .current_session_id
            .clone()
            .unwrap_or_else(|| Uuid::new_v4().to_string());
        let user_msg = Message::user(session_id.clone(), user_message.clone());
        self.messages.push(user_msg);

        // Show that we're processing
        self.status_message = "🤔 Grok is thinking...".to_string();
        self.render()?;

        // Prepare messages for API (including conversation history)
        let api_messages: Vec<ApiMessage> = self
            .messages
            .iter()
            .map(|msg| ApiMessage {
                role: msg.role.to_string(),
                content: msg.content.clone(),
            })
            .collect();

        // Send to API using direct HTTP client (similar to main.rs)
        match self.send_to_grok_api(api_messages).await {
            Ok(response_content) => {
                // Add assistant response to UI
                let assistant_msg = Message::assistant(
                    session_id,
                    response_content.clone(),
                    Some(self.selected_model.clone()),
                );
                self.messages.push(assistant_msg);

                self.status_message = "✅ Message sent! Press 'i' to continue chatting.".to_string();
            }
            Err(e) => {
                // Show error in UI
                let error_msg = Message::assistant(
                    session_id,
                    format!("❌ Error: {}", e),
                    Some("error".to_string()),
                );
                self.messages.push(error_msg);
                self.status_message = "❌ Error occurred. Check your API key and try again.".to_string();
            }
        }
        Ok(())
    }

    async fn send_to_grok_api(&self, messages: Vec<ApiMessage>) -> Result<String> {
        use reqwest::Client;
        use tokio::time::{timeout, Duration};

        let client = Client::new();

        let request_body = serde_json::json!({
            "messages": messages,
            "model": self.selected_model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": false
        });

        // Add timeout to prevent hanging
        let response = timeout(
            Duration::from_secs(60), // 60 second timeout
            client
                .post("https://api.x.ai/v1/chat/completions")
                .header("Authorization", format!("Bearer {}", self.api_key))
                .header("Content-Type", "application/json")
                .json(&request_body)
                .send()
        ).await??;

        if !response.status().is_success() {
            let status = response.status();
            let error_text = response.text().await.unwrap_or_default();
            return Err(anyhow::anyhow!("❌ API Error ({}): {}", status, error_text));
        }

        let response_json: serde_json::Value = response.json().await?;

        let content = response_json["choices"]
            .get(0)
            .and_then(|choice| choice["message"]["content"].as_str())
            .ok_or_else(|| anyhow::anyhow!("❌ No response content found in API response"))?;

        Ok(content.to_string())
    }

    async fn create_new_session(&mut self) -> Result<()> {
        let session_id = Uuid::new_v4().to_string();
        self.current_session_id = Some(session_id.clone());
        self.messages.clear();
        self.status_message = format!("✨ New session created: {}", session_id);
        Ok(())
    }

    fn cycle_model(&mut self) {
        let current_index = self
            .available_models
            .iter()
            .position(|m| m == &self.selected_model)
            .unwrap_or(0);

        let next_index = (current_index + 1) % self.available_models.len();
        self.selected_model = self.available_models[next_index].clone();
        self.status_message = format!("Model changed to: {}", self.selected_model);
    }

    fn load_session_list(&mut self) -> Result<()> {
        // This would load existing sessions - simplified for now
        self.status_message = "Session list loading not implemented yet.".to_string();
        Ok(())
    }

    fn render(&mut self) -> Result<()> {
        let messages = &self.messages;
        let input_buffer = &self.input_buffer;
        let input_mode = self.input_mode.clone();
        let selected_model = &self.selected_model;
        let status_message = &self.status_message;
        let show_help = self.show_help;

        self.terminal.draw(|f| {
            let size = f.size();

            // Create main layout
            let chunks = Layout::default()
                .direction(Direction::Vertical)
                .constraints([
                    Constraint::Min(1),    // Messages area
                    Constraint::Length(3), // Input area
                    Constraint::Length(3), // Status bar
                ])
                .split(size);

            // Render messages
            ChatUI::render_messages(f, chunks[0], messages);

            // Render input area
            ChatUI::render_input(f, chunks[1], input_buffer, input_mode);

            // Render status bar
            ChatUI::render_status_bar(f, chunks[2], selected_model, status_message);

            // Render help if needed
            if show_help {
                ChatUI::render_help(f, size);
            }
        })?;

        Ok(())
    }

    fn render_messages(f: &mut Frame, area: Rect, messages: &[Message]) {
        let messages: Vec<ListItem> = messages
            .iter()
            .map(|msg| {
                let role = match msg.role {
                    MessageRole::User => Span::styled(
                        "You: ",
                        Style::default()
                            .fg(Color::Blue)
                            .add_modifier(Modifier::BOLD),
                    ),
                    MessageRole::Assistant => Span::styled(
                        "Grok: ",
                        Style::default()
                            .fg(Color::Green)
                            .add_modifier(Modifier::BOLD),
                    ),
                    MessageRole::System => Span::styled(
                        "System: ",
                        Style::default()
                            .fg(Color::Yellow)
                            .add_modifier(Modifier::BOLD),
                    ),
                };

                // For long messages, we need to wrap them properly
                let content_lines: Vec<Line> = if msg.content.len() > 50 {
                    // Split long messages into multiple lines
                    msg.content
                        .chars()
                        .collect::<Vec<_>>()
                        .chunks(50)
                        .map(|chunk| Line::from(Span::raw(chunk.iter().collect::<String>())))
                        .collect()
                } else {
                    vec![Line::from(Span::raw(&msg.content))]
                };

                // Create the main line with role
                let mut lines = vec![Line::from(vec![role.clone()])];
                lines.extend(content_lines);

                ListItem::new(lines).style(Style::default().fg(Color::White))
            })
            .collect();

        let messages_list = List::new(messages)
            .block(Block::default().borders(Borders::ALL).title("💬 Chat"))
            .highlight_style(Style::default().add_modifier(Modifier::BOLD));

        f.render_widget(messages_list, area);
    }

    fn render_input(f: &mut Frame, area: Rect, input_buffer: &str, input_mode: InputMode) {
        let input = Paragraph::new(input_buffer)
            .style(match input_mode {
                InputMode::Insert => Style::default().fg(Color::White),
                InputMode::Normal => Style::default().fg(Color::Gray),
            })
            .block(Block::default().borders(Borders::ALL).title("Input"))
            .wrap(Wrap { trim: true });

        f.render_widget(input, area);
    }

    fn render_status_bar(f: &mut Frame, area: Rect, selected_model: &str, status_message: &str) {
        let status_parts = vec![
            Span::styled("Model: ", Style::default().fg(Color::Cyan)),
            Span::styled(selected_model, Style::default().fg(Color::White)),
            Span::raw(" | "),
            Span::styled(status_message, Style::default().fg(Color::Gray)),
        ];

        let status = Paragraph::new(Line::from(status_parts))
            .block(Block::default().borders(Borders::ALL).title("Status"))
            .wrap(Wrap { trim: true });

        f.render_widget(status, area);
    }

    fn render_help(f: &mut Frame, area: Rect) {
        let help_text = vec![
            Line::from(vec![Span::styled(
                "Help",
                Style::default().add_modifier(Modifier::BOLD),
            )]),
            Line::from(""),
            Line::from(vec![Span::styled(
                "Normal Mode:",
                Style::default().fg(Color::Yellow),
            )]),
            Line::from("  i - Enter insert mode"),
            Line::from("  q - Quit"),
            Line::from("  h - Toggle help"),
            Line::from("  c - Create new session"),
            Line::from("  m - Cycle model"),
            Line::from("  l - Load sessions"),
            Line::from(""),
            Line::from(vec![Span::styled(
                "Insert Mode:",
                Style::default().fg(Color::Yellow),
            )]),
            Line::from("  Enter - Send message"),
            Line::from("  Esc - Return to normal mode"),
            Line::from("  Type your message..."),
            Line::from(""),
            Line::from("Press any key to close help..."),
        ];

        let help = Paragraph::new(help_text)
            .block(Block::default().borders(Borders::ALL).title("Help"))
            .style(Style::default().fg(Color::White))
            .wrap(Wrap { trim: true });

        let help_area = Rect {
            x: area.width / 4,
            y: area.height / 4,
            width: area.width / 2,
            height: area.height / 2,
        };

        f.render_widget(Clear, help_area);
        f.render_widget(help, help_area);
    }
}

pub async fn run_terminal_chat(session_id: Option<String>, model: String) -> Result<()> {
    let mut ui = ChatUI::new().await?;

    if let Some(sid) = session_id {
        ui.current_session_id = Some(sid.clone());
        ui.status_message = format!("🔄 Resumed session: {}", sid);
    }

    ui.selected_model = model;
    ui.run().await
}

fn setup_terminal() -> Result<AppTerminal> {
    let mut stdout = io::stdout();
    enable_raw_mode()?;
    execute!(stdout, EnterAlternateScreen, EnableMouseCapture)?;
    let backend = CrosstermBackend::new(stdout);
    let terminal = AppTerminal::new(backend)?;

    Ok(terminal)
}

fn restore_terminal(terminal: &mut AppTerminal) -> Result<()> {
    disable_raw_mode()?;
    execute!(
        terminal.backend_mut(),
        LeaveAlternateScreen,
        DisableMouseCapture
    )?;
    terminal.show_cursor()?;

    Ok(())
}

impl Drop for ChatUI {
    fn drop(&mut self) {
        let _ = restore_terminal(&mut self.terminal);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_input_mode() {
        assert_eq!(InputMode::Normal, InputMode::Normal);
        assert_ne!(InputMode::Normal, InputMode::Insert);
    }

    #[test]
    fn test_message_formatting() {
        let message = Message::user("session-123".to_string(), "Hello".to_string());
        assert_eq!(message.role, MessageRole::User);
        assert_eq!(message.content, "Hello");
    }
}
