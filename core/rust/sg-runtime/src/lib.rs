//! SuperGrok runtime: registry load, intent route, skill markdown, binary stubs.
//!
//! Skills live at `core/skills/<category>/<role>/SKILL.md`.
//! Registry: `core/skills/_framework/REGISTRY.json`.

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};

pub type SgId = String;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SuperGrokMeta {
    pub sg_id: SgId,
    pub name: String,
    pub category: String,
    #[serde(default)]
    pub role: String,
    pub tier: String,
    #[serde(default)]
    pub title: String,
    #[serde(default)]
    pub shorthand: String,
    #[serde(default)]
    pub intent: String,
    #[serde(default)]
    pub purpose: String,
    pub binary_id: String,
    pub path: String,
    #[serde(default)]
    pub nest: String,
    #[serde(default)]
    pub call: String,
    #[serde(default)]
    pub intent_tags: Vec<String>,
    #[serde(default)]
    pub kind: String,
    #[serde(default)]
    pub when_to_use: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SuperGrokRegistry {
    pub version: String,
    pub leslie_gate: String,
    #[serde(default)]
    pub skills_root: String,
    #[serde(default)]
    pub layout: String,
    pub count: usize,
    pub categories: Vec<String>,
    pub skills: Vec<SuperGrokMeta>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SgOutput {
    pub sg_id: SgId,
    pub name: String,
    pub win: String,
    pub message: String,
    #[serde(default)]
    pub artifacts: Vec<String>,
}

#[derive(Debug)]
pub enum SuperGrokError {
    Io(std::io::Error),
    Json(serde_json::Error),
    NotFound(String),
    BinaryStub(String),
}

impl std::fmt::Display for SuperGrokError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            SuperGrokError::Io(e) => write!(f, "registry io: {e}"),
            SuperGrokError::Json(e) => write!(f, "registry json: {e}"),
            SuperGrokError::NotFound(n) => write!(f, "unknown supergrak: {n}"),
            SuperGrokError::BinaryStub(id) => write!(f, "binary not implemented: {id}"),
        }
    }
}

impl std::error::Error for SuperGrokError {}
impl From<std::io::Error> for SuperGrokError {
    fn from(e: std::io::Error) -> Self {
        SuperGrokError::Io(e)
    }
}
impl From<serde_json::Error> for SuperGrokError {
    fn from(e: serde_json::Error) -> Self {
        SuperGrokError::Json(e)
    }
}

#[derive(Debug, Default)]
pub struct SuperGrokIndex {
    pub registry: Option<SuperGrokRegistry>,
    by_name: HashMap<String, SuperGrokMeta>,
    by_id: HashMap<String, SuperGrokMeta>,
    by_category: HashMap<String, Vec<String>>,
}

impl SuperGrokIndex {
    pub fn load_from_repo_root(repo_root: impl AsRef<Path>) -> Result<Self, SuperGrokError> {
        let path = repo_root
            .as_ref()
            .join("core/skills/_framework/REGISTRY.json");
        Self::load_path(path)
    }

    pub fn load_path(path: impl AsRef<Path>) -> Result<Self, SuperGrokError> {
        let raw = fs::read_to_string(path)?;
        let registry: SuperGrokRegistry = serde_json::from_str(&raw)?;
        let mut idx = SuperGrokIndex {
            registry: Some(registry.clone()),
            ..Default::default()
        };
        for sk in registry.skills {
            idx.by_category
                .entry(sk.category.clone())
                .or_default()
                .push(sk.name.clone());
            idx.by_id.insert(sk.sg_id.clone(), sk.clone());
            idx.by_name.insert(sk.name.clone(), sk);
        }
        Ok(idx)
    }

    pub fn get(&self, name_or_id: &str) -> Option<&SuperGrokMeta> {
        self.by_name
            .get(name_or_id)
            .or_else(|| self.by_id.get(name_or_id))
    }

    pub fn by_category(&self, category: &str) -> Vec<&SuperGrokMeta> {
        self.by_category
            .get(category)
            .into_iter()
            .flatten()
            .filter_map(|n| self.by_name.get(n))
            .collect()
    }

    pub fn list_categories(&self) -> Vec<String> {
        let mut cats: Vec<String> = self.by_category.keys().cloned().collect();
        cats.sort();
        cats
    }

    pub fn route(&self, intent: &str, limit: usize) -> Vec<&SuperGrokMeta> {
        let intent_l = intent.to_lowercase();
        let tokens: Vec<&str> = intent_l
            .split(|c: char| !c.is_alphanumeric() && c != '-')
            .filter(|t| t.len() > 2)
            .collect();

        let mut scored: Vec<(i32, &SuperGrokMeta)> = self
            .by_name
            .values()
            .map(|sk| {
                let mut score = 0i32;
                for t in &tokens {
                    if sk.name.contains(t) {
                        score += 5;
                    }
                    if sk.category == *t {
                        score += 4;
                    }
                    if sk.nest.contains(t) {
                        score += 3;
                    }
                    if sk.intent.to_lowercase().contains(t) {
                        score += 2;
                    }
                    for tag in &sk.intent_tags {
                        if tag == t || tag.contains(t) {
                            score += 3;
                        }
                    }
                }
                (score, sk)
            })
            .filter(|(s, _)| *s > 0)
            .collect();

        scored.sort_by(|a, b| b.0.cmp(&a.0).then_with(|| a.1.name.cmp(&b.1.name)));
        scored.into_iter().take(limit).map(|(_, sk)| sk).collect()
    }

    pub fn skill_md_path(&self, repo_root: impl AsRef<Path>, name: &str) -> Option<PathBuf> {
        let meta = self.get(name)?;
        Some(repo_root.as_ref().join(&meta.path))
    }
}

/// Future native entrypoints. v1 always stubs.
pub fn run_binary(meta: &SuperGrokMeta, _ctx_json: &str) -> Result<SgOutput, SuperGrokError> {
    Err(SuperGrokError::BinaryStub(meta.binary_id.clone()))
}

pub fn load_skill_markdown(
    repo_root: impl AsRef<Path>,
    index: &SuperGrokIndex,
    name: &str,
) -> Result<String, SuperGrokError> {
    let path = index
        .skill_md_path(repo_root, name)
        .ok_or_else(|| SuperGrokError::NotFound(name.to_string()))?;
    Ok(fs::read_to_string(path)?)
}

/// MCP-facing summary of one skill.
#[derive(Debug, Clone, Serialize)]
pub struct McpSkillDescriptor {
    pub name: String,
    pub sg_id: String,
    pub call: String,
    pub category: String,
    pub nest: String,
    pub intent: String,
    pub purpose: String,
    pub binary_id: String,
    pub path: String,
}

impl SuperGrokIndex {
    pub fn mcp_descriptors(&self) -> Vec<McpSkillDescriptor> {
        let mut out: Vec<_> = self
            .by_name
            .values()
            .map(|sk| McpSkillDescriptor {
                name: sk.name.clone(),
                sg_id: sk.sg_id.clone(),
                call: if sk.call.is_empty() {
                    format!("/{}", sk.name)
                } else {
                    sk.call.clone()
                },
                category: sk.category.clone(),
                nest: sk.nest.clone(),
                intent: sk.intent.clone(),
                purpose: sk.purpose.clone(),
                binary_id: sk.binary_id.clone(),
                path: sk.path.clone(),
            })
            .collect();
        out.sort_by(|a, b| a.name.cmp(&b.name));
        out
    }
}
