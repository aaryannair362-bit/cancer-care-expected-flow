#!/bin/bash
cd "$(dirname "$0")"
echo "CCA Cancer Care AI OS V12.2-PC4.0 — Clinician Validation"
echo "Open http://127.0.0.1:${PORT:-8765}  |  Demo PIN: 2026"
echo "Validation feedback is saved in the local demo database until reset_demo.py is run."
PORT="${PORT:-8765}" python3 server.py
