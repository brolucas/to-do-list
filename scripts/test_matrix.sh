#!/bin/bash

# Versions de Python à tester
python_versions=("3.13" "3.9" "2.7")

# Versions de Django à tester
django_versions=("5" "4" )

# Dossier pour stocker les environnements virtuels
base_dir="envs"

# Créer un dossier de base pour les environnements virtuels
mkdir -p $base_dir

# Fonction pour tester une version de Python et Django
test_python_django() {
    local python_version=$1
    local django_version=$2

    # Créer un environnement virtuel pour la combinaison Python/Django
    env_dir="$base_dir/env_${python_version}_django_${django_version}"
    mkdir -p $env_dir
    cd $env_dir

    # Installer la version de Python via pyenv si nécessaire
    echo "==== Installation de Python $python_version ===="
    pyenv install -s $python_version
    pyenv local $python_version

    # Créer un environnement virtuel
    python -m venv venv
    source venv/bin/activate

    # Installer Django spécifique
    echo "==== Installation de Django $django_version ===="
    pip install "django==$django_version"

    # Lancer les tests
    echo "==== Lancement des tests avec Python $python_version et Django $django_version ===="
    python manage.py test  # Remplacez par votre commande de test spécifique

    # Désactivation de l'environnement virtuel
    deactivate
    cd - > /dev/null  # Revenir au répertoire initial
}

# Test pour chaque combinaison de Python et Django
for python_version in "${python_versions[@]}"; do
    for django_version in "${django_versions[@]}"; do
        test_python_django $python_version $django_version
    done
done

echo "Tests terminés pour toutes les combinaisons."
