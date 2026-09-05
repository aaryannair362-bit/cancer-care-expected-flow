#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parent
for stem in ['cca_v12.sqlite3','cca_v11.sqlite3','cca_v10.sqlite3']:
    for suffix in ['', '-shm', '-wal']:
        p=ROOT/(stem+suffix)
        if p.exists(): p.unlink()
from server import init_db
init_db()
print('CCA V12.2 Final Defect Remediation demo data reset.')
