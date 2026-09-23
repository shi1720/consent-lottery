"""Optional source retrieval for literature inspection; not needed for results."""
import hashlib
import json
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'literature/downloads';dest.mkdir(exist_ok=True)
sources=json.loads((ROOT/'literature/sources.json').read_text())
for name,record in sources.items():
    response=requests.get(record['url'],timeout=90)
    response.raise_for_status()
    suffix='.pdf' if response.content.startswith(b'%PDF') else '.html'
    (dest/(name+suffix)).write_bytes(response.content)
    sha=hashlib.sha256(response.content).hexdigest()
    print(name,'matches recorded source' if sha==record['sha256'] else 'SOURCE CHANGED: inspect before relying on the archived audit')
