#!/bin/bash
# Remove Russian translation from Raycast.
set -euo pipefail
APP="${APP:-/Applications/Raycast.app}"
FE="$APP/Contents/Resources/macos-app_RaycastDesktopApp.bundle/Contents/Resources/frontend"
for f in "$FE"/*.html; do
  /usr/bin/sed -i '' 's|<script src="./ru-dict.js"></script><script src="./ru-translate.js"></script>||' "$f"
done
rm -f "$FE/ru-dict.js" "$FE/ru-translate.js"
echo "Перевод удалён. Перезапустите Raycast."
