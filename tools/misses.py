#!/usr/bin/env python3
"""Collect strings that ru-translate.js saw on screen but could not translate.

Reads them from Raycast's WebKit localStorage (a copy, never the live file) and
prints "English<TAB>" lines ready to be filled in and appended to tr/ru.tsv.
The list may include your own data (file names, app names) — skip those.
"""
import glob, json, os, shutil, sqlite3, sys, tempfile
ROOT = os.path.expanduser('~/Library/WebKit/com.raycast.macos/WebsiteData')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_dict import D, load_tsv
known = set(load_tsv(f'{D}/tr/ru.tsv'))
out = set()
for db in glob.glob(ROOT + '/**/localstorage.sqlite3', recursive=True):
    tmp = tempfile.mkdtemp()
    for ext in ('', '-wal', '-shm'):  # copy so the live database is never touched
        if os.path.exists(db + ext): shutil.copy(db + ext, f'{tmp}/l.sqlite3{ext}')
    try:
        row = sqlite3.connect(f'{tmp}/l.sqlite3').execute(
            "select value from ItemTable where key='ru-translate-misses'").fetchone()
    except sqlite3.Error:
        row = None
    shutil.rmtree(tmp)
    if row:
        v = row[0]
        v = v.decode('utf-16-le') if isinstance(v, bytes) else v
        out |= set(json.loads(v))
new = sorted(out - known)
for s in new:
    print(s.replace('\n', '\\n') + '\t')
print(f'{len(new)} untranslated', file=sys.stderr)
