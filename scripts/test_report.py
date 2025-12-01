# scripts/test_report.py
import yaml
import json

# Chargement du YAML
with open("test_list.yaml", "r", encoding="utf-8") as f:
    test_list = yaml.safe_load(f)

# Chargement du JSON
try:
    with open("result_test_auto.json", "r", encoding="utf-8") as f:
        result_json = json.load(f)
        print("Lecture des tests auto via result_test_auto.json…\nOK\n")
except FileNotFoundError:
    print("result_test_auto.json introuvable !")
    result_json = {"tests": []}

# Créer un dict id -> status pour lookup rapide
status_map = {t["id"]: t["status"] for t in result_json.get("tests", [])}

# Fonction pour déterminer le statut
def display_status(test_id, test_type):
    if test_type.lower() == "auto":
        if test_id in status_map:
            return "✅Passed" if status_map[test_id] == "passed" else "❌Failed"
        else:
            return "🕳Not found"
    else:  # manuel
        return "🫱Manual test needed"

# Liste de tous les tests avec leur statut pour calcul statistique
all_tests = []

# Parcours des tests Auto
for test in test_list.get("Auto", []):
    test_id = test.get("id")
    status = display_status(test_id, 'auto')
    print(f"{test_id} | auto | {status}")
    all_tests.append(status)

# Parcours des tests Manuel
for test in test_list.get("Manuel", []):
    test_id = test.get("id")
    status = display_status(test_id, 'manuel')
    print(f"{test_id} | manuel | {status}")
    all_tests.append(status)

# Calcul des statistiques
total = len(all_tests)
passed = all_tests.count("✅Passed")
failed = all_tests.count("❌Failed")
not_found = all_tests.count("🕳Not found")
manual = all_tests.count("🫱Manual test needed")
passed_plus_manual = passed + manual

# Affichage du rapport
print("\nNumber of tests:", total)
print(f"✅Passed tests: {passed} ({passed/total*100:.1f}%)")
print(f"❌Failed tests: {failed} ({failed/total*100:.1f}%)")
print(f"🕳Not found tests: {not_found} ({not_found/total*100:.1f}%)")
print(f"🫱Test to pass manually: {manual} ({manual/total*100:.1f}%)")
print(f"✅Passed + 🫱Manual: {passed_plus_manual} ({passed_plus_manual/total*100:.1f}%)")
