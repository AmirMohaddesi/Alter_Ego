---
title: Career_Conversation
app_file: app.py
sdk: gradio
sdk_version: 5.34.2
---

# Alter Ego

**Alter Ego** is a small, production-minded **Gradio chat demo** that answers career and background questions in a fixed persona, grounded in **local documents** you control. It uses OpenAI function calling for lightweight lead capture and “unknown question” logging (optional Pushover), and it is designed to **deploy cleanly on Hugging Face Spaces** without brittle local assumptions.

- **Live demo:** [Hugging Face Space](https://huggingface.co/spaces/AMIXXM/Career_Conversation)
- **Stack:** Python · Gradio · OpenAI Chat Completions · `pypdf` (read-only PDF text)
- **Audience:** recruiters, collaborators, and portfolio reviewers who want grounded answers, not a generic chatbot

## How it works

1. On startup, the app loads **`me/summary.txt`** and, if present, extracts text from **`me/linkedin.pdf`** and **`me/resume.pdf`** (read-only).
2. That text is injected into a **system prompt** so the model stays in character and cites your real profile material.
3. Each user message is sent to **OpenAI** with **tools** for recording an email (`record_user_details`) and logging unanswered questions (`record_unknown_question`). Tool handlers may send **Pushover** notifications when credentials are set.
4. If **`OPENAI_API_KEY`** is missing, the Space still **starts**; chat returns a clear **demo-mode** message instead of failing at import or first request.

## Modes

| Mode | `OPENAI_API_KEY` | Profile files | Behavior |
|------|------------------|---------------|----------|
| **Personal** | Set | Your `me/summary.txt` + optional PDFs | Full AI replies grounded on your files; tools active when the model calls them. |
| **Demo** | Unset | Any (missing PDFs OK) | UI loads; each reply explains that the Space needs API secrets for live answers. |

Protected inputs: **`me/resume.pdf`** and **`me/linkedin.pdf`** are **never written** by this app—only read. There is **no** code path that saves or overwrites them.

## Why This Project

Most personal profile bots are either generic or hard to maintain. This project keeps the stack intentionally small while supporting:

- persona-grounded responses from local files
- lightweight tool calling for lead capture and unknown-question logging
- local run plus Hugging Face Spaces deployment

## Core Features

- **Grounded context ingestion** from `me/summary.txt` and optional PDFs
- **Function tools** for:
  - recording contact details (`record_user_details`)
  - logging unanswered questions (`record_unknown_question`)
- **Optional Pushover notifications** for interaction events
- **Fail-safe startup behavior** when PDFs are missing or unparsable

## Architecture Overview

Single-process Gradio app (`app.py`) with one main class:

1. `Me.__init__` loads profile context from local files.
2. `Me.system_prompt()` builds persona and context instructions.
3. `Me.chat()` runs OpenAI chat-completions with function tools.
4. Tool calls dispatch to local Python functions and optionally notify via Pushover.

This design is intentionally simple and easy to fork for other personas.

## Repository Layout

```text
.
├─ app.py
├─ requirements.txt
├─ .env.example
├─ .gitignore
├─ scripts/
│  └─ smoke_gradio_build.py
├─ outputs/              # reserved for future exports; app does not write profile PDFs here
├─ tests/
│  └─ test_app.py
├─ me/
│  ├─ summary.txt
│  ├─ resume.pdf         # optional; your copy — add with -f if .gitignore excludes it
│  └─ linkedin.pdf       # optional; your copy — add with -f if .gitignore excludes it
└─ README.md
```

**Git and your PDFs:** `.gitignore` may exclude `me/*.pdf` so you can keep them local-only. To **ship the same PDFs to Hugging Face** via git, force-add once: `git add -f me/resume.pdf me/linkedin.pdf` then commit and push. The application never modifies those files.

## Setup

### 1) Create and activate environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment variables

Copy and edit:

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Required variable:
- `OPENAI_API_KEY`

Optional variables:
- `OPENAI_MODEL` (default: `gpt-4o-mini`)
- `PUSHOVER_TOKEN`
- `PUSHOVER_USER`

## Quickstart

```bash
python app.py
```

Then open the local Gradio URL shown in the terminal.

## Example Usage

Try prompts such as:
- "What are your strongest robotics and ML skills?"
- "Can you summarize your recent projects?"
- "How can I contact you for collaboration?"

Expected output:
- grounded answers based on local profile docs
- possible follow-up request for contact details
- unknown-question tool logging when context is insufficient

## Validation

```bash
pytest -q
```

Optional one-shot **deployment smoke** (no server listen, no API key):

```bash
python scripts/smoke_gradio_build.py
```

Tests cover PDF missing-file fallback, tool email validation, demo-mode chat message, Gradio interface construction without secrets, and safe `Me()` bootstrap.

## Deployment (Hugging Face Spaces)

**SDK:** **Gradio** (declared in this file’s YAML front matter: `sdk: gradio`, `app_file: app.py`). Hugging Face runs `app.py` and Gradio serves the UI—no Streamlit or Docker required for this repo.

1. Create or open a **Gradio** Space linked to this GitHub repo (or push this repo to `huggingface.co/spaces/...`).
2. Ensure **`app.py`** remains the entry file; keep **`requirements.txt`** aligned with pinned deps.
3. **Settings → Variables and secrets:** set **`OPENAI_API_KEY`** for personal/live mode. Optional: **`OPENAI_MODEL`**, **`PUSHOVER_TOKEN`**, **`PUSHOVER_USER`**.
4. Rebuild or **Factory reboot** the Space after changing secrets.
5. Confirm behavior: with key → real answers; without key → demo-mode message, app still healthy.

### Profile files on the Space

- If **`me/resume.pdf`** / **`me/linkedin.pdf`** are in the Space repository, their extracted text is used in the system prompt.
- If they are absent or not text-extractable, startup still succeeds; **`me/summary.txt`** remains the primary fallback text source.
- **Read-only guarantee:** the codebase never opens these PDFs for writing and has no logic that persists chat or profile data into `me/`.

## Limitations

- Context quality depends on `me/summary.txt` and provided PDFs.
- No persistence layer for tool outputs yet (notifications only).
- No end-to-end tests against live OpenAI/Pushover APIs.

## Roadmap

- Add persistent storage for captured leads and unknown questions.
- Add prompt/context regression tests (beyond current smoke and unit tests).
- Add optional structured conversation analytics.

## GitHub repository metadata

Suggested **description** (short, for the GitHub “About” box):

> Gradio + OpenAI persona chat grounded in local resume/summary PDFs; Hugging Face Spaces–ready, with demo mode when API keys are absent.

Suggested **topics** (`About` → Topics):

`gradio` `openai` `chatbot` `huggingface-spaces` `python` `llm` `persona` `portfolio` `resume` `pypdf`

## Project Status

Active personal portfolio project. Production-hardening in progress with emphasis on reproducibility and clear developer onboarding.

## License

MIT (see `LICENSE`).
