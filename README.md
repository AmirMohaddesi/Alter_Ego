---
title: Career_Conversation
app_file: app.py
sdk: gradio
sdk_version: 5.34.2
---

# Alter Ego

Portfolio-style conversational agent that answers questions as a professional profile persona, grounded in local source documents (`me/summary.txt`, optional resume PDF, optional LinkedIn PDF).

- Live demo: [Hugging Face Space](https://huggingface.co/spaces/AMIXXM/Career_Conversation)
- Runtime: Python + Gradio + OpenAI Chat Completions
- Primary use case: recruiter/client-facing Q&A assistant for a personal site

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
├─ tests/
│  └─ test_app.py
├─ me/
│  └─ summary.txt
└─ README.md
```

Optional files (not committed by default):
- `me/resume.pdf`
- `me/linkedin.pdf`

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

### Local modes

- **Personal mode (full behavior):** set `OPENAI_API_KEY` and keep your profile files in `me/`.
- **Demo mode (degraded):** if `OPENAI_API_KEY` is not set, the app still starts and returns a clear demo-mode message instead of crashing.

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

Run the included sanity tests:

```bash
pytest -q
```

These tests verify core non-network behaviors (PDF loading fallback and email validation tool behavior).

## Deployment (Hugging Face Spaces)

### Target type

This project should be deployed as a **Gradio Space**:
- `sdk: gradio` is defined in the README front matter
- `app_file: app.py` is the active entrypoint

### Steps

1. Create a new Space with SDK type **Gradio**.
2. Push this repository as-is (keep `app.py` as the entrypoint).
3. In Space settings -> **Variables and secrets**, set:
   - required: `OPENAI_API_KEY` (for full AI responses)
   - optional: `OPENAI_MODEL`, `PUSHOVER_TOKEN`, `PUSHOVER_USER`
4. Restart/rebuild the Space.

### Profile file behavior (`me/resume.pdf`, `me/linkedin.pdf`)

- If present, these files are loaded and used as grounding context.
- If missing/unparseable, startup continues safely and the app falls back to `me/summary.txt`.
- The app only reads these files; it does not write, modify, or overwrite them.

## Limitations

- Context quality depends on `me/summary.txt` and provided PDFs.
- No persistence layer for tool outputs yet (notifications only).
- No end-to-end tests against live OpenAI/Pushover APIs.

## Roadmap

- Add persistent storage for captured leads and unknown questions.
- Add prompt/context regression tests.
- Add CI workflow for test + lint checks.
- Add optional structured conversation analytics.

## Project Status

Active personal portfolio project. Production-hardening in progress with emphasis on reproducibility and clear developer onboarding.

## License

MIT (see `LICENSE`).
