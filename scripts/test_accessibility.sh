#!/bin/bash

URLS=(
  "http://localhost:8000/"
  "http://localhost:8000/tasks/"
  "http://localhost:8000/about/"
)

mkdir -p accessibility-reports

ALL_PASS=true

for URL in "${URLS[@]}"; do
    REPORT_FILE="accessibility-reports/$(echo $URL | sed 's|https\?://||; s|/|_|g').html"
    echo "Testing $URL ..."

    pa11y "$URL" --standard WCAG2A --reporter html > "$REPORT_FILE"

    if [ $? -ne 0 ]; then
        echo "🚨 Accessibilité échouée pour $URL"
        ALL_PASS=false
    else
        echo "✅ Accessibilité OK pour $URL"
    fi
done

if [ "$ALL_PASS" = false ]; then
    echo "❌ Certaines pages n'ont pas passé le test WCAG 2.1 niveau A."
    exit 1
else
    echo "✅ Toutes les pages passent le test WCAG 2.1 niveau A !"
fi
