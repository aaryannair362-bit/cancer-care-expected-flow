import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from server import H, init_db

init_db()


class handler(H):
    pass
