#!/usr/bin/env python3
"""Deployment smoke check: import app and build Gradio UI without OPENAI_API_KEY.

Run from repo root:
  python scripts/smoke_gradio_build.py
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    os.environ.pop("OPENAI_API_KEY", None)

    import app as app_module  # noqa: PLC0415 — after path/env setup

    app_module.create_chat_interface()
    print("smoke_gradio_build: OK (ChatInterface constructed, demo-mode safe)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
