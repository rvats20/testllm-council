# ⚡ Quick Start Guide

Get LLM Council running in 5 minutes!

## Prerequisites

- Python 3.8+
- Anthropic API key (get one at https://console.anthropic.com/)

## Setup Steps

### 1. Clone or Download

```bash
# If from GitHub
git clone https://github.com/YOUR_USERNAME/llm-council.git
cd llm-council

# Or download and extract the ZIP file
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set API Key

**Option A: Environment Variable (Recommended)**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-api-key-here"
```

**Option B: .env File**
```bash
cp .env.example .env
# Edit .env and add your API key
```

### 4. Run Test

```bash
python test_council.py
```

If you see "✅ ALL TESTS PASSED", you're good to go!

### 5. Run Example

```bash
python council.py
```

This will:
- Generate 3 agent responses
- Have 2 judges evaluate them
- Output a decision with confidence score
- Save `decision.json` and `audit_log.json`

### 6. Try the UI (Optional)

```bash
python app.py
```

Then open http://localhost:7860 in your browser.

## Your First Custom Query

```python
from council import LLMCouncil

# Initialize
council = LLMCouncil()

# Your question
query = "Should I use microservices or monolithic architecture for my startup?"

# Get decision
decision = council.run_council(query)

# See the winner
print(f"Winner: {decision.winner}")
print(f"Confidence: {decision.confidence:.2%}")
```

## Common Issues

### "No module named 'anthropic'"
```bash
pip install anthropic
```

### "API key not found"
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### "Rate limit exceeded"
- Wait a minute and try again
- Or use a smaller query

## Next Steps

1. ✅ Read the full [README.md](README.md)
2. 🚀 Deploy to [Hugging Face](HUGGINGFACE_DEPLOYMENT.md)
3. 📦 Push to [GitHub](GITHUB_DEPLOYMENT.md)
4. 🛠️ Customize agent personas in `council.py`
5. ⚙️ Adjust safety thresholds
6. 📊 Analyze audit logs

## Quick Reference

### Run Council
```python
from council import LLMCouncil
council = LLMCouncil()
decision = council.run_council("Your query here")
```

### Check Decision
```python
print(decision.winner)           # Winning agent
print(decision.confidence)       # Confidence score (0-1)
print(decision.safety_gate_status)  # APPROVED/REQUIRES_APPROVAL/BLOCKED
print(decision.risks)            # List of identified risks
```

### Save Outputs
```python
council.save_decision(decision, "my_decision.json")
council.save_audit_log("my_audit.json")
```

### Change Model
```python
council = LLMCouncil(model="claude-sonnet-4-20250514")
```

## Example Queries to Try

- "What's the best way to learn machine learning?"
- "Should I use SQL or NoSQL for my application?"
- "How do I implement OAuth2 authentication?"
- "What are the pros and cons of serverless architecture?"
- "Explain how Docker containers work"

## Get Help

- 📖 Read the [full documentation](README.md)
- 🐛 [Open an issue](https://github.com/YOUR_USERNAME/llm-council/issues) on GitHub
- 💬 Check the [Discussions](https://github.com/YOUR_USERNAME/llm-council/discussions)

Happy experimenting! 🏛️
