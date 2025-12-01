#!/usr/bin/env bash
set -euo pipefail  # Active l'arrêt en cas d'erreur, vérification des variables non définies et pipefail

# Usage: ./buicld.sh version=1.0.1
arg="${1:-}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Vérification de l'argument version
if [[ -z "$arg" || "$arg" != version=* ]]; then
  echo "Usage: ./build.sh version=x.y.z" >&2
  exit 1
fi
VERSION="${arg#version=}"

# Vérification que la version est au format x.y.z
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Version '$VERSION' invalide (attendu x.y.z)" >&2
  exit 1
fi

SETTINGS_PATH="todo/settings.py"

# Vérification de l'existence du fichier settings.py
if [[ ! -f "$SETTINGS_PATH" ]]; then
  echo "Fichier introuvable: $SETTINGS_PATH" >&2
  exit 1
fi

# Vérification du lint avec Ruff
echo "Vérification du lint (Ruff)..."
if command -v pipenv >/dev/null 2>&1; then
  pipenv run ruff check .
elif [[ -x ".venv/bin/ruff" ]]; then
  .venv/bin/ruff check .
elif [[ -x ".venv/Scripts/ruff.exe" ]]; then
  .venv/Scripts/ruff.exe check .
else
  echo "Ruff introuvable. Installez les dépendances (pipenv install) avant de lancer le build." >&2
  exit 1
fi

# Exécution de la matrice de tests
echo "Exécution de la matrice de tests..."
if [[ -x "$SCRIPT_DIR/test_matrix.sh" ]]; then
  bash "$SCRIPT_DIR/test_matrix.sh"
else
  echo "scripts/test_matrix.sh introuvable ou non exécutable" >&2
  exit 1
fi

# Vérification si le tag existe déjà
if git tag --list "$VERSION" | grep -q .; then
  echo "Le tag '$VERSION' existe déjà" >&2
  exit 1
fi

# Mise à jour de la version dans settings.py
python - <<PY
from pathlib import Path
import re, sys

version = "$VERSION"
path = Path("$SETTINGS_PATH")
text = path.read_text()
new_text, count = re.subn(r"VERSION\s*=\s*['\"]([^'\"]*)['\"]", f"VERSION = '{version}'", text, count=1)
if count == 0:
    sys.exit("Aucune assignation VERSION trouvée")
path.write_text(new_text)
PY

# Ajout, commit et création du tag Git
git add -A
git commit -m "Bump version to $VERSION"
git tag -a "$VERSION" -m "Version $VERSION"

# Création de l'archive
ARCHIVE_NAME="todolist-$VERSION.zip"
git archive --format=zip --output "$ARCHIVE_NAME" --prefix="todolist-$VERSION/" HEAD

# Confirmation de la version créée
echo "Version $VERSION créée :"
echo " - settings mis à jour et commit"
echo " - tag '$VERSION' créé"
echo " - archive générée : $ARCHIVE_NAME"
