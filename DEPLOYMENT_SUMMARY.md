# 🎉 LLM Council - Complete Package

Your minimal LLM Council system is ready for deployment!

## 📦 What's Included

### Core Files
✅ **council.py** - Main council logic with 3 agents + 2 judges
✅ **app.py** - Gradio UI for Hugging Face Spaces
✅ **test_council.py** - Test suite to verify everything works
✅ **requirements.txt** - All Python dependencies

### Documentation
✅ **README.md** - Complete project documentation
✅ **QUICKSTART.md** - Get started in 5 minutes
✅ **ARCHITECTURE.md** - System design and data flow
✅ **GITHUB_DEPLOYMENT.md** - Step-by-step GitHub setup
✅ **HUGGINGFACE_DEPLOYMENT.md** - Step-by-step HF Spaces setup
✅ **DEPLOYMENT_CHECKLIST.md** - Complete deployment checklist

### Configuration
✅ **.gitignore** - Git ignore rules
✅ **.env.example** - API key template
✅ **LICENSE** - MIT License

## 🚀 Quick Start (30 seconds)

```bash
# 1. Navigate to the folder
cd llm-council

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API key
export ANTHROPIC_API_KEY="sk-ant-your-key"

# 4. Run test
python test_council.py

# 5. Run example
python council.py
```

## 📊 System Overview

**Input:** User query
**Process:** 
- 3 agents generate responses (Analytical, Creative, Practical)
- 2 judges evaluate and score (Primary, Secondary)
- Winner determined by vote aggregation
- Safety gate checks confidence and risks
**Output:** Decision Object (JSON) + Audit Log (JSON)

## 🎯 Key Features Implemented

✅ **3 Respondent Agents** - Different perspectives on each query
✅ **2 Judge Agents** - Evaluate using structured rubric
✅ **Decision Object** - JSON with winner, confidence, risks, citations
✅ **Safety Gating** - APPROVED / REQUIRES_APPROVAL / BLOCKED
✅ **Audit Logging** - Complete trail saved to disk
✅ **Gradio UI** - Optional web interface (bonus!)

## 📈 Next Steps

### 1. Deploy to GitHub (5 minutes)
```bash
cd llm-council
git init
git add .
git commit -m "Initial commit: LLM Council"
gh repo create llm-council --public --source=. --remote=origin --push
```

See [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) for details.

### 2. Deploy to Hugging Face (5 minutes)
1. Go to https://huggingface.co/spaces
2. Create new Space (Gradio SDK)
3. Upload: app.py, council.py, requirements.txt, README.md
4. Wait for build
5. Test at https://huggingface.co/spaces/YOUR_USERNAME/llm-council

See [HUGGINGFACE_DEPLOYMENT.md](HUGGINGFACE_DEPLOYMENT.md) for details.

### 3. Customize (Optional)
- Modify agent personas in `council.py`
- Adjust safety thresholds in `safety_gate()` method
- Add more agents or judges
- Customize the evaluation rubric
- Add support for other LLM providers

## 🔒 Security Reminders

- ⚠️ Never commit your API key
- ✅ Use environment variables or .env file
- ✅ Add .env to .gitignore (already done)
- ✅ Use repository secrets on HF Spaces for production

## 📚 Documentation Structure

```
llm-council/
├── README.md              ← Start here
├── QUICKSTART.md          ← Get running in 5 min
├── ARCHITECTURE.md        ← System design
├── GITHUB_DEPLOYMENT.md   ← GitHub setup
├── HUGGINGFACE_DEPLOYMENT.md  ← HF Spaces setup
├── DEPLOYMENT_CHECKLIST.md    ← Complete checklist
├── council.py             ← Main code
├── app.py                 ← Gradio UI
├── test_council.py        ← Tests
└── requirements.txt       ← Dependencies
```

## 💡 Example Usage

### Python API
```python
from council import LLMCouncil

council = LLMCouncil()
decision = council.run_council("Should I use microservices?")

print(f"Winner: {decision.winner}")
print(f"Confidence: {decision.confidence:.2%}")
print(f"Safety: {decision.safety_gate_status}")
```

### Command Line
```bash
python council.py
```

### Web UI
```bash
python app.py
# Open http://localhost:7860
```

## 📊 Cost & Performance

**Per Query:**
- API Calls: 5 (3 agents + 2 judges)
- Tokens: ~6,000 total
- Cost: ~$0.05-0.10 (Anthropic Sonnet 4)
- Time: 10-20 seconds (with parallelization possible)

## 🛠️ Troubleshooting

**"No module named 'anthropic'"**
→ Run: `pip install -r requirements.txt`

**"API key not found"**
→ Run: `export ANTHROPIC_API_KEY="sk-ant-..."`

**"Import error: council"**
→ Make sure you're in the llm-council directory

**Gradio not starting**
→ Check port 7860 is free: `lsof -i :7860`

## 🎓 Learning Resources

- [Anthropic API Docs](https://docs.anthropic.com/)
- [Gradio Documentation](https://gradio.app/docs/)
- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)
- [Safety in AI Systems](https://www.anthropic.com/safety)

## 🤝 Contributing

Want to improve the council?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Ideas for contributions:
- Add more agent types
- Implement different LLM providers
- Enhance the evaluation rubric
- Add visualization tools
- Improve safety gating logic
- Add API rate limiting
- Create Docker container

## 📞 Support

- 📖 Read the documentation
- 🐛 Open a GitHub issue
- 💬 Start a discussion
- 📧 Contact: [Your contact info]

## ✨ What Makes This Special

**Minimal but Complete:**
- Only 2 Python files for core functionality
- No unnecessary dependencies
- Clear, readable code
- Production-ready structure

**Safe by Design:**
- Multi-tier safety gating
- Comprehensive audit logging
- Risk assessment built-in
- Transparent decision making

**Easy to Deploy:**
- One-command GitHub push
- Drag-and-drop HF Spaces
- No server setup needed
- Works out of the box

**Highly Extensible:**
- Add agents in minutes
- Customize evaluation criteria
- Plug in different LLMs
- Build on solid foundation

## 🏆 Success Metrics

You'll know it's working when:
- ✅ Test script passes all checks
- ✅ Example query returns a decision
- ✅ decision.json file is created
- ✅ audit_log.json contains full trail
- ✅ Safety gate status is displayed
- ✅ Gradio UI loads and works

## 🎨 Customization Examples

### Add a Security-Focused Agent
```python
agents.append({
    "id": "agent_security",
    "system": "You are a security expert. Identify potential vulnerabilities and risks."
})
```

### Make Safety Gate Stricter
```python
def safety_gate(self, confidence, risks, avg_safety):
    if avg_safety < 8:  # Raised from 6
        return "BLOCKED"
    elif confidence < 0.7:  # Raised from 0.5
        return "REQUIRES_APPROVAL"
    else:
        return "APPROVED"
```

### Add Custom Metrics
```python
@dataclass
class JudgeScore:
    # ... existing fields ...
    bias_score: float  # New field
    clarity_score: float  # New field
```

## 📝 License

MIT License - Free to use, modify, and distribute.

## 🙏 Acknowledgments

Built with:
- Anthropic Claude API
- Gradio for UI
- Python for everything

---

**Ready to deploy?** Follow the deployment checklist and you'll be live in minutes!

**Questions?** Check the documentation or open an issue.

**Happy building!** 🏛️✨
