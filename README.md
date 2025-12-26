# 🏛️ LLM Council

A minimal multi-agent decision system with safety gating and audit logging. Three specialized agents generate responses, two judges evaluate them, and a final decision is produced with confidence scoring and risk assessment.

## 🎯 Features

- **3 Respondent Agents**: Analytical, Creative, and Practical perspectives
- **2 Judge Agents**: Primary and secondary evaluation with scoring rubrics
- **Safety Gating**: Automatic blocking or approval requirements based on confidence and safety scores
- **Structured Decision Object**: JSON output with winner, confidence, risks, and citations
- **Audit Logging**: Complete trail of all agent outputs, judge scores, and final decisions
- **Gradio UI**: Optional web interface for Hugging Face Spaces

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/llm-council.git
cd llm-council

# Install dependencies
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

## 🚀 Usage

### Command Line

```python
from council import LLMCouncil

# Initialize council
council = LLMCouncil()

# Run council on a query
query = "What are the best practices for implementing secure authentication?"
decision = council.run_council(query)

# Save outputs
council.save_decision(decision, "decision.json")
council.save_audit_log("audit_log.json")
```

### Run the example

```bash
python council.py
```

### Gradio UI

```bash
python app.py
```

Then open http://localhost:7860 in your browser.

## 📊 Decision Object Structure

```json
{
  "winner": "agent_analytical",
  "confidence": 0.85,
  "risks": ["Low confidence from judge_secondary"],
  "citations": ["agent_analytical: Contains citations"],
  "agent_responses": [...],
  "judge_scores": [...],
  "safety_gate_status": "APPROVED",
  "timestamp": "2025-12-26T10:30:00"
}
```

## 🔒 Safety Gating

The system implements three-tier safety gating:

- **APPROVED**: Confidence ≥ 0.5, safety score ≥ 6, risks ≤ 2
- **REQUIRES_APPROVAL**: Confidence < 0.5 OR risks > 2
- **BLOCKED**: Safety score < 6

## 📋 Audit Log

Complete audit trail saved to `audit_log.json`:

```json
[
  {
    "type": "agent_response",
    "data": {
      "agent_id": "agent_analytical",
      "response": "...",
      "timestamp": "..."
    }
  },
  {
    "type": "judge_score",
    "data": {
      "judge_id": "judge_primary",
      "winner": "agent_analytical",
      "confidence": 0.85,
      ...
    }
  },
  {
    "type": "final_decision",
    "data": {...}
  }
]
```

## 🎨 Judge Evaluation Rubric

Each judge scores responses on:

1. **Accuracy** (0-10): Factual correctness and logical soundness
2. **Safety** (0-10): Absence of harmful or biased content
3. **Completeness** (0-10): Thoroughness in addressing the query

## 🌐 Deploy to Hugging Face Spaces

1. Create a new Space at https://huggingface.co/spaces
2. Select "Gradio" as the SDK
3. Upload all files from this repository
4. Add your `ANTHROPIC_API_KEY` as a Space secret (Settings → Repository secrets)
5. The Space will automatically build and launch

Alternatively, users can enter their API key directly in the UI.

## 🔧 Configuration

### Change LLM Model

```python
council = LLMCouncil(model="claude-sonnet-4-20250514")
```

### Customize Agent Personas

Edit the `generate_agent_responses()` method in `council.py` to modify agent system prompts.

### Adjust Safety Thresholds

Modify the `safety_gate()` method thresholds:

```python
def safety_gate(self, confidence: float, risks: List[str], avg_safety: float) -> str:
    if avg_safety < 6:  # Adjust this threshold
        return "BLOCKED"
    elif confidence < 0.5:  # Adjust this threshold
        return "REQUIRES_APPROVAL"
    else:
        return "APPROVED"
```

## 📂 File Structure

```
llm-council/
├── council.py          # Main council logic
├── app.py             # Gradio UI
├── requirements.txt   # Python dependencies
├── README.md          # This file
├── decision.json      # Output: Final decision (generated)
└── audit_log.json     # Output: Audit trail (generated)
```

## 🧪 Example Output

**Query**: "What are the best practices for implementing secure authentication?"

**Decision Summary**:
- Winner: `agent_analytical`
- Confidence: 87%
- Safety Gate: APPROVED
- Risks: None identified
- Citations: agent_analytical contains references to OWASP guidelines

## 🛠️ Development

### Add More Agents

```python
agents = [
    {
        "id": "agent_security",
        "system": "You are a security-focused agent. Prioritize safety and threat mitigation."
    },
    # Add more agents here
]
```

### Add More Judges

```python
judges = [
    {"id": "judge_technical", "system": "Focus on technical accuracy"},
    {"id": "judge_ethical", "system": "Focus on ethical implications"},
    # Add more judges here
]
```

## 📝 License

MIT License - feel free to use and modify as needed.

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a PR.

## 🔗 Links

- GitHub: https://github.com/YOUR_USERNAME/llm-council
- Hugging Face Space: https://huggingface.co/spaces/YOUR_USERNAME/llm-council

## ⚠️ Disclaimer

This is a minimal implementation for demonstration and experimentation. For production use, consider:

- More robust error handling
- Rate limiting and cost controls
- Database persistence for audit logs
- Authentication and authorization
- More sophisticated safety checks
- Multi-provider LLM support
