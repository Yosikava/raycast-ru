#!/usr/bin/env python3
"""List UI strings from the installed Raycast that are missing in tr/ru.tsv.

Prints "English<TAB>" lines ready to be filled in and appended to tr/ru.tsv.
Run after a Raycast update to find new strings.
"""
import glob, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_dict import D, load_tsv

APP = os.environ.get('APP', '/Applications/Raycast.app')
R = APP + '/Contents/Resources/macos-app_RaycastDesktopApp.bundle/Contents/Resources'
# Property keys whose string values are shown in the UI.
KEYS = set('''title description label children message text placeholder displayName sidebarTitle
reason tooltip headerTitle searchPlaceholder subtitle required userMessage summary intro failureTitle
commandsTitle accessory badge content actionLabel feedbackTitle extensionLabel tag settingsLabel
groupLabel atLimit nearLimit errorMessage macos one prompt alt'''.split())
LIT = re.compile(r'([A-Za-z_$][\w$]*)\s*:\s*(?:`([^`$\\]{2,400})`|"((?:[^"\\\n]|\\.){2,400})")')
BAD = re.compile(r'[{}<>=;|\[\]@#^*_]|https?:|\.(js|ts|css|png|svg|json|mjs)\b|^[a-z0-9.-]+$|^[a-z]+[A-Z]\w*$|^[A-Z_0-9]+$')

def ui_strings():
    found = set()
    for f in glob.glob(R + '/frontend/*.js') + [R + '/backend/index.mjs']:
        src = open(f, encoding='utf-8', errors='replace').read()
        for m in LIT.finditer(src):
            s = (m.group(2) or m.group(3)).strip()
            if m.group(1) in KEYS and re.match(r'[A-Z0-9]', s) and re.search(r'[a-z]{2}', s) and not BAD.search(s):
                found.add(s)
    return found

if __name__ == '__main__':
    known = load_tsv(f'{D}/tr/ru.tsv')
    new = sorted(ui_strings() - set(known), key=str.lower)
    for s in new:
        print(s.replace('\n', '\\n') + '\t')
    print(f'{len(new)} strings not in tr/ru.tsv', file=sys.stderr)
