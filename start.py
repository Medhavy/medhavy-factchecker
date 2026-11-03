#!/usr/bin/env python3
"""start.py — one command to open the review dashboard.

    python3 start.py          (Windows: py start.py)

First run: creates a private Python environment in .venv and installs Streamlit (about a minute). After that it just
starts. The dashboard opens in your browser at http://localhost:8501 and runs only on your own computer (it listens on 127.0.0.1, so nobody else on the network can reach it).
"""
import subprocess, sys, venv
from pathlib import Path

REPO = Path(__file__).resolve().parent
VENV = REPO / ".venv"
PY = VENV / ("Scripts/python.exe" if sys.platform.startswith("win") else "bin/python")

if sys.version_info < (3, 9):
    sys.exit("Python 3.9 or newer is needed.")
if not PY.exists():
    print("First run: creating a private environment in .venv ...")
    venv.create(VENV, with_pip=True)
if subprocess.run([str(PY), "-c", "import streamlit"], capture_output=True).returncode != 0:
    print("Installing Streamlit (one time) ...")
    subprocess.check_call([str(PY), "-m", "pip", "install", "-q", "-r", str(REPO / "requirements.txt")])
print("Starting the review dashboard. Press Ctrl+C here to stop it.")
sys.exit(subprocess.call([str(PY), "-m", "streamlit", "run", str(REPO / "review_app.py"),
                          "--server.address", "127.0.0.1", "--browser.gatherUsageStats", "false"], cwd=REPO))
