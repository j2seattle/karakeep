"""Print item count per list (counts only)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from kk_client import Client

c = Client()
s, d = c.rest("GET", "/lists")
for l in d["lists"]:
    n = sum(1 for _ in c.paged(f"/lists/{l['id']}/bookmarks?includeContent=false", "bookmarks", "limit=100"))
    print(f"{l['type']:6} {n:4}  {l['name']}  [{l.get('query') or ''}]")
