---
title: Career_Conversation
app_file: app.py
sdk: gradio
sdk_version: 5.34.2
---

# Alter Ego — Amir (Gradio + OpenAI)

**Live demo:** https://huggingface.co/spaces/AMIXXM/Career_Conversation

This project is a conversational AI agent that represents **Amirhosein Mohaddesi**, providing answers about his background, skills, and projects.  
It runs locally or as a **Hugging Face Space** using Gradio.

> Note: The files `me/resume.pdf` and `me/linkedin.pdf` are placeholders.  
> Replace them with your own public or redacted versions to personalize the Alter Ego.

---

## Overview

Alter Ego uses Gradio for interaction and OpenAI's API for generating responses.  
The agent also includes small "tool" calls for recording user contact details and logging unknown questions for later improvement.

Key capabilities:
- Persona-grounded answers (based on local profile text and PDFs)
- Deployed seamlessly via Hugging Face Spaces
- Uses `.env` for secrets (safe configuration)
- Optional Pushover notifications for new user interactions

---

## Repository Structure
```
.
├─ app.py
├─ requirements.txt
├─ .env.example
├─ me/
│  ├─ summary.txt
│  ├─ resume.pdf        # placeholder
│  └─ linkedin.pdf      # placeholder
└─ README.md
```

---

## Environment Variables

Before running, create a `.env` file in the root directory (copy from `.env.example`) and fill the following:

| Variable | Required | Description |
|-----------|-----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `PUSHOVER_TOKEN` | No | Optional, for receiving push notifications |
| `PUSHOVER_USER`  | No | Optional, for Pushover user ID |
| `HUGGINGFACEHUB_API_TOKEN` | No | Required only if calling Hugging Face Inference APIs directly |

---

## Local Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Open .env and add your keys

python app.py
# The terminal will show a local Gradio URL to open in your browser
```

---

## Deploy on Hugging Face Spaces

### Using the Web Interface
1. Create a new **Gradio Space** on Hugging Face.
2. Upload `app.py`, `requirements.txt`, `.env.example`, and `me/summary.txt`.
3. In your Space settings, go to **Variables and secrets** and add:
   - `OPENAI_API_KEY`
   - (Optional) `PUSHOVER_TOKEN`, `PUSHOVER_USER`
4. Commit and the Space will build automatically.

### Using Gradio Deploy
If you used `gradio deploy`, keep the YAML header at the top of this README (already included).

---

## Example Prompts
- "What are Amir’s most notable ROS2 multi-robot projects?"
- "How does Amir integrate human navigation data into his AI agents?"
- "Can I leave my contact info for a follow-up?"

---

## Troubleshooting
- **No chat response:** Ensure `OPENAI_API_KEY` is set correctly.
- **PDF parsing error:** Use text-based (non-image) PDFs or rely only on `summary.txt`.
- **Pushover errors:** Leave optional variables empty if not using notifications.

---

## Credits
Created by **Amirhosein Mohaddesi** as part of **Ed Donner’s Udemy course**.  
Mentioned with permission for feedback and endorsement.

---

## License
MIT License
