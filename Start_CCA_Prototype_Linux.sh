#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
PORT="${PORT:-8765}" python3 server.py
