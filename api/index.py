import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from server import H, init_db

init_db()

_PREFIX = '/api/index'


class handler(H):
    def _restore_path(self):
        # vercel.json rewrites "/(.*)" -> "/api/index/$1" so the app's own
        # path-based router (which reads self.path) sees the real route
        # instead of the literal rewrite destination.
        parsed = urlparse(self.path)
        path = parsed.path
        if path.startswith(_PREFIX):
            path = path[len(_PREFIX):] or '/'
        self.path = urlunparse(('', '', path, '', parsed.query, ''))

    def do_GET(self):
        self._restore_path()
        return super().do_GET()

    def do_POST(self):
        self._restore_path()
        return super().do_POST()
