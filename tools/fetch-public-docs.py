#!/usr/bin/env python3
"""Download allowlisted official documents into public/docs/ (offline library).
Falls back gracefully: if a URL fails, the doc is skipped and noted (app links to official page instead)."""
import json, urllib.request, ssl
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "public" / "docs"
DOCS.mkdir(parents=True, exist_ok=True)

# Allowlisted stable URLs (official OHCHR/UN). docstore links can be session-bound → verified at fetch time.
DOCS_TO_FETCH = [
    # (file, list of candidate URLs)
    ("GA-Res-60-251.pdf", [
        "https://www2.ohchr.org/english/bodies/hrcouncil/docs/a.res.60.251_en.pdf",
        "https://documents.un.org/doc/un/doc/res/gen/undoc/gen/g06/117/83/pdf/g0611783.pdf",
    ]),
    ("A-RES-76-300.pdf", [
        "https://documents.un.org/doc/undoc/gen/n22/289/80/pdf/n2228980.pdf",
    ]),
]

ctx = ssl.create_default_context()
manifest_path = ROOT / "src" / "data" / "docs-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
fetched, failed = [], []

for file, urls in DOCS_TO_FETCH:
    dest = DOCS / file
    ok = False
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (education)"})
            with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
                data = r.read()
            if data[:4] == b"%PDF" and len(data) > 10000:
                dest.write_bytes(data)
                print(f"  OK  {file}  ({len(data)//1024} KB)  <- {url}")
                fetched.append(file); ok = True
                break
            else:
                print(f"  SKIP {url} (not a PDF / too small)")
        except Exception as e:
            print(f"  FAIL {url}: {e}")
    if not ok:
        failed.append(file)

# update manifest: mark which docs are actually available offline
for d in manifest:
    d["offline"] = (d["file"] in fetched)
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

print(f"\nFetched: {len(fetched)}, failed/skipped: {len(failed)}")
if failed:
    print("Failed (app falls back to official landing links):", ", ".join(failed))
