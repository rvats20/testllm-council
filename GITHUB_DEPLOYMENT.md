# GitHub Deployment Guide

## 1. Create GitHub Repository

```bash
# Navigate to project directory
cd llm-council

# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: LLM Council multi-agent system"

# Create repository on GitHub (via web interface or gh cli)
# Then link your local repo:
git remote add origin https://github.com/YOUR_USERNAME/llm-council.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 2. Using GitHub CLI (Alternative)

```bash
# Install GitHub CLI if you haven't: https://cli.github.com/

# Navigate to project directory
cd llm-council

# Initialize and push in one command
gh repo create llm-council --public --source=. --remote=origin --push

# Or for private repo
gh repo create llm-council --private --source=. --remote=origin --push
```

## 3. Repository Settings

### Add Description
- Go to your repo on GitHub
- Click "Edit" next to "About"
- Add: "Multi-agent LLM decision system with safety gating and audit logging"
- Add topics: `llm`, `multi-agent`, `ai`, `claude`, `anthropic`, `safety`, `gradio`

### Add License (Optional)
```bash
# Add MIT license
curl https://raw.githubusercontent.com/licenses/license-templates/master/templates/mit.txt > LICENSE

# Edit LICENSE file to add your name and year
# Then commit
git add LICENSE
git commit -m "Add MIT license"
git push
```

## 4. Verify Files

Your repository should contain:
- ✅ council.py
- ✅ app.py
- ✅ requirements.txt
- ✅ README.md
- ✅ .gitignore
- ✅ .env.example
- ✅ GITHUB_DEPLOYMENT.md (this file)
- ✅ HUGGINGFACE_DEPLOYMENT.md

## 5. Test Clone

```bash
# Test that someone can clone and run your project
cd /tmp
git clone https://github.com/YOUR_USERNAME/llm-council.git
cd llm-council
pip install -r requirements.txt
python council.py
```

## 6. Add Secrets (for GitHub Actions - Optional)

If you want to add CI/CD:
1. Go to repo Settings → Secrets and variables → Actions
2. Add `ANTHROPIC_API_KEY` secret
3. Create `.github/workflows/test.yml` for automated testing

## 7. Update README Links

After creating the repository, update these placeholders in README.md:
- Replace `YOUR_USERNAME` with your GitHub username
- Update the GitHub link in the "Links" section

## Quick Setup Commands

```bash
# Full setup in one go
cd llm-council
git init
git add .
git commit -m "Initial commit: LLM Council multi-agent system"
gh repo create llm-council --public --source=. --remote=origin --push
```

## Troubleshooting

**Error: "remote origin already exists"**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/llm-council.git
```

**Error: "refusing to merge unrelated histories"**
```bash
git pull origin main --allow-unrelated-histories
```

**Large files warning**
Make sure `decision.json` and `audit_log.json` are in `.gitignore` to avoid committing large output files.
