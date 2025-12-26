# Hugging Face Spaces Deployment Guide

## Method 1: Web Interface (Easiest)

### 1. Create New Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in details:
   - **Space name**: `llm-council`
   - **License**: MIT
   - **SDK**: Gradio
   - **Hardware**: CPU (free tier is sufficient)
   - **Visibility**: Public or Private

### 2. Upload Files

After creating the Space, upload these files directly via the web interface:
- ✅ `app.py`
- ✅ `council.py`
- ✅ `requirements.txt`
- ✅ `README.md`

### 3. Configure Space

The Space will automatically detect `app.py` as the Gradio application and start building.

### 4. Add API Key (Optional)

**Option A: Repository Secret (Recommended for production)**
1. Go to Space Settings → Repository secrets
2. Add secret: `ANTHROPIC_API_KEY` = `sk-ant-your-key`
3. Modify `app.py` to read from environment:

```python
import os
default_api_key = os.getenv("ANTHROPIC_API_KEY", "")
```

**Option B: User Input (Recommended for public demos)**
- Keep the current implementation where users enter their own API key
- This is already set up in `app.py`

### 5. Wait for Build

The Space will automatically:
- Install dependencies from `requirements.txt`
- Launch the Gradio app
- Provide a public URL: `https://huggingface.co/spaces/YOUR_USERNAME/llm-council`

## Method 2: Git Push (Advanced)

### 1. Install Git LFS

```bash
git lfs install
```

### 2. Clone Your Space

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/llm-council
cd llm-council
```

### 3. Copy Files

```bash
# Copy from your llm-council directory
cp /path/to/llm-council/*.py .
cp /path/to/llm-council/requirements.txt .
cp /path/to/llm-council/README.md .
```

### 4. Push to Hugging Face

```bash
git add .
git commit -m "Initial commit: LLM Council"
git push
```

## Method 3: Clone from GitHub (Recommended)

### 1. Create Space Linked to GitHub

1. Create new Space on Hugging Face
2. After creation, go to Space Settings → Git repository
3. Enable "Linked to a GitHub repository"
4. Connect to your `llm-council` GitHub repo
5. Hugging Face will automatically sync with your GitHub repo

**Benefits:**
- Single source of truth (GitHub)
- Automatic updates when you push to GitHub
- Easy to maintain

## Post-Deployment Configuration

### 1. Update Space README

Create or update `README.md` in your Space with:

```markdown
---
title: LLM Council
emoji: 🏛️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# 🏛️ LLM Council

Multi-agent decision system with safety gating...
[Rest of your README content]
```

### 2. Test Your Space

1. Visit `https://huggingface.co/spaces/YOUR_USERNAME/llm-council`
2. Enter your Anthropic API key (or use environment secret)
3. Test with a sample query
4. Verify outputs appear correctly

### 3. Share Your Space

- Get shareable link: `https://huggingface.co/spaces/YOUR_USERNAME/llm-council`
- Embed in websites using the embed code
- Share on social media

## Advanced: Custom Domain

1. Go to Space Settings → Custom domain
2. Add your domain (requires Hugging Face Pro)
3. Update DNS records as instructed

## Troubleshooting

### "Application startup failed"

Check the Logs tab in your Space. Common issues:

**Missing dependencies:**
```bash
# Add to requirements.txt
anthropic>=0.39.0
gradio>=4.0.0
```

**Import errors:**
```python
# Make sure council.py is in the same directory as app.py
from council import LLMCouncil
```

### "API key not working"

**If using environment secrets:**
```python
import os
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment")
```

**If using user input:**
```python
# Already handled in app.py - users enter their own key
```

### Space is slow

- Upgrade to GPU or better CPU (Settings → Hardware)
- Add caching for LLM calls
- Reduce max_tokens in council.py

### Want to add authentication?

```python
demo.launch(auth=("username", "password"))
```

## Monitoring

1. **Logs**: Check real-time logs in Space Settings → Logs
2. **Analytics**: View usage in Space Settings → Analytics
3. **Community**: Enable discussions for user feedback

## Update Your Space

### From GitHub (if linked):
```bash
# Just push to GitHub, HF syncs automatically
git push origin main
```

### Direct upload:
1. Go to Files tab in your Space
2. Upload updated files
3. Space will rebuild automatically

## Space Configuration Options

Create `config.yaml` for advanced settings:

```yaml
title: LLM Council
emoji: 🏛️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
python_version: 3.11
fullWidth: true
models:
  - anthropic/claude-sonnet-4
```

## Example Spaces for Reference

- Gradio Demos: https://huggingface.co/spaces/gradio/demos
- Multi-agent examples: Search "multi-agent" on HF Spaces

## Final Checklist

- ✅ Space created and files uploaded
- ✅ requirements.txt includes all dependencies
- ✅ API key configured (secret or user input)
- ✅ Test run completed successfully
- ✅ README updated with Space URL
- ✅ GitHub repo linked (optional)
- ✅ Space made public (if desired)

Your Space URL will be:
**https://huggingface.co/spaces/YOUR_USERNAME/llm-council**

Share this link and let people try your LLM Council! 🚀
