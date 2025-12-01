# tasks/tests_runner.py
import json
from datetime import datetime
from django.test.runner import DiscoverRunner
import unittest

class JsonTestResult(unittest.TextTestResult):
    """Custom result that records test_case_id and status."""
    def __init__(self, stream=None, descriptions=True, verbosity=1):
        super().__init__(stream, descriptions, verbosity)
        self.test_results = []

    def addSuccess(self, test):
        test_id = getattr(test, 'test_case_id', None)
        if test_id:
            self.test_results.append({"id": test_id, "status": "Passed"})
        super().addSuccess(test)

    def addFailure(self, test, err):
        test_id = getattr(test, 'test_case_id', None)
        if test_id:
            self.test_results.append({"id": test_id, "status": "Failed"})
        super().addFailure(test, err)

    def addError(self, test, err):
        test_id = getattr(test, 'test_case_id', None)
        if test_id:
            self.test_results.append({"id": test_id, "status": "Error"})
        super().addError(test, err)


class JsonTestRunner(DiscoverRunner):
    """Runner Django qui écrit les résultats dans un JSON"""
    output_file = "result_test_auto.json"

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        """Construire la suite de tests complète"""
        suite = super().build_suite(test_labels, extra_tests, **kwargs)
        return suite

    def run_suite(self, suite, **kwargs):
        """Exécute la suite avec notre JsonTestResult"""
        result = JsonTestResult()
        suite.run(result)

        # Génération JSON
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump({
                "date": datetime.utcnow().isoformat(),
                "tests": result.test_results
            }, f, indent=4)
        print(f"\n[JsonTestRunner] JSON généré : {self.output_file}")

        # Retourne le nombre de tests échoués
        return len(result.failures) + len(result.errors)
