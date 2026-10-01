#!/bin/bash
# Install Russian translation into Raycast. Safe to re-run after Raycast updates.
set -euo pipefail
APP="${APP:-/Applications/Raycast.app}"
FE="$APP/Contents/Resources/macos-app_RaycastDesktopApp.bundle/Contents/Resources/frontend"
DIR="$(cd "$(dirname "$0")" && pwd)"
[ -d "$FE" ] || { echo "Не найден интерфейс Raycast 2.x: $FE"; exit 1; }
cp "$DIR/src/ru-dict.js" "$DIR/src/ru-translate.js" "$FE/"
TAG='<script src="./ru-dict.js"></script><script src="./ru-translate.js"></script>'
for f in "$FE"/*.html; do
  grep -q 'ru-translate.js' "$f" || /usr/bin/sed -i '' "s|<head>|<head>$TAG|" "$f"
done
echo "Готово. Перезапустите Raycast (Quit Raycast в строке меню)."
