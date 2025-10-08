# 🤖 Grok AI Assistant - n8n Custom Node

**Embed xAI's Grok intelligence directly into your n8n workflows.**

## ✨ Features

- **Chat Completion** - AI responses in your workflow
- **Workflow Analysis** - AI analyzes and suggests optimizations
- **Data Enhancement** - AI transforms and enriches data
- **Node Configuration** - AI generates node parameters

## 🚀 Installation

### Method 1: Copy to n8n custom nodes

```bash
# Copy to your n8n instance
cp -r n8n-nodes/grok-ai-assistant ~/.n8n/custom/

# Restart n8n
pkill -f n8n && npx n8n start
```

### Method 2: Install as npm package

```bash
cd ~/.n8n/custom
npm install n8n-nodes-grok-ai-assistant
```

## 🎯 Usage Examples

### 1. Chat Completion

**Use Case**: Get AI insights on data

**Config**:
- Operation: Chat Completion
- Model: grok-4-fast
- Prompt: "Analyze this sales data and identify trends"
- Include Input Data: Yes

**Input**: `{sales: [...]}`
**Output**: AI analysis with insights

### 2. Workflow Analysis

**Use Case**: Optimize your workflow

**Config**:
- Operation: Analyze Workflow
- Model: grok-4-0709

**Input**: Workflow data from previous nodes
**Output**: Optimization suggestions

### 3. Data Enhancement

**Use Case**: Enrich incoming data

**Config**:
- Operation: Enhance Data
- Prompt: "Extract email, phone, and classify as lead quality"

**Input**: Raw customer data
**Output**: Enhanced with AI insights

## 🔧 Advanced Features

- **Temperature Control** - Adjust creativity (0-2)
- **Max Tokens** - Control response length
- **System Prompts** - Custom AI behavior
- **Error Handling** - Continue on fail option
- **Token Usage** - Track API costs

## 📖 Models Available

- **grok-4-0709** - Most capable, thorough analysis
- **grok-4-fast** - Fast and accurate (recommended)
- **grok-3-mini** - Fastest, low cost
- **grok-code-fast-1** - Specialized for code

## 💡 Tips

- Use **Grok-4-fast** for best speed/quality balance
- Enable **Include Input Data** to give AI context
- Set **Temperature** low (0.2-0.5) for factual tasks
- Use **System Prompt** to customize AI behavior

## 🎨 Integration with OPGROK

This node is part of the OPGROK ecosystem and works seamlessly with:
- OPGROK Workflow Builder (http://localhost:8000/workflows)
- n8n local instance (http://localhost:5678)
- Grok Chat Interface

## 📝 License

MIT - See LICENSE file
