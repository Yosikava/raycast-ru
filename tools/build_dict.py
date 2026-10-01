#!/usr/bin/env python3
"""Build src/ru-dict.js from tr/ru.tsv and tr/patterns.json."""
import json, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

def load_tsv(path):
    d = {}
    for n, line in enumerate(open(path, encoding='utf-8'), 1):
        line = line.rstrip('\n')
        if not line or line.startswith('#'):
            continue
        if '\t' not in line:
            raise SystemExit(f'{path}:{n}: no TAB between English and Russian')
        en, ru = line.split('\t', 1)
        if en in d and d[en] != ru:
            print(f'{path}:{n}: duplicate "{en}", last one wins')
        d[en.replace('\\n', '\n')] = ru.replace('\\n', '\n')
    return d

if __name__ == '__main__':
    d = load_tsv(f'{D}/tr/ru.tsv')
    pats = json.load(open(f'{D}/tr/patterns.json', encoding='utf-8'))
    with open(f'{D}/src/ru-dict.js', 'w', encoding='utf-8') as f:
        f.write('window.__RU_DICT = ' + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + ';\n')
        f.write('window.__RU_PATTERNS = ' + json.dumps(pats, ensure_ascii=False) + ';\n')
    print(len(d), 'entries,', len(pats), 'patterns')
