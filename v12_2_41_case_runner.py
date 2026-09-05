#!/usr/bin/env python3
"""Compatibility entry point for the canonical V12.2 synthetic 41-case runner.

The prior implementation of this filename used stale assumptions and produced false
failures. The canonical scenario pack is now v12_2_synthetic_41_case_runner.py.
"""
from pathlib import Path
import runpy

CANONICAL = Path(__file__).with_name("v12_2_synthetic_41_case_runner.py")
runpy.run_path(str(CANONICAL), run_name="__main__")
