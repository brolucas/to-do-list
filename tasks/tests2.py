from django.test import TestCase
from django.urls import reverse
from .models import Task
import os
from django.core.management import call_command

class TaskModelTest(TestCase):
    def test_str_returns_title(self):
        task = Task(title="My task")

        self.assertEqual(str(task), "My task")


class TaskViewsTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Demo task")

    def test_homepage_renders(self):
        response = self.client.get(reverse("list"))
        self.assertEqual(response.status_code, 200)

    def test_create_task_via_post(self):
        response = self.client.post(reverse("list"), {"title": "New task"})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="New task").exists())

    def test_update_page_renders(self):
        response = self.client.get(reverse("update_task", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    def test_update_task_via_post(self):
        response = self.client.post(
            reverse("update_task", args=[self.task.id]),
            {"title": "Updated title"},
        )

        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated title")

    def test_delete_page_renders(self):
        response = self.client.get(reverse("delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_task_via_post(self):
        response = self.client.post(reverse("delete", args=[self.task.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


class EntryPointModulesTest(TestCase):
    def test_wsgi_module_imports(self):
        from todo import wsgi

        self.assertIsNotNone(wsgi.application)

    def test_asgi_module_imports(self):
        from todo import asgi

        self.assertIsNotNone(asgi.application)



class FixturesTest(TestCase):
    def test_fixture_import(self):
        """Teste l'import du fichier JSON et vérifie que les tâches sont en base"""

        # Chemin complet vers la fixture
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'dataset.json')

        # Charger la fixture
        call_command('loaddata', fixture_path, verbosity=0)

        # Vérifier qu'il y a bien des tâches importées
        self.assertTrue(Task.objects.exists(), "Aucune tâche n'a été importée")

        # Optionnel : vérifier une tâche spécifique
        self.assertTrue(
            Task.objects.filter(title="Buy groceries").exists(),
            "La tâche 'Buy groceries' n'a pas été importée"
        )

        # Optionnel : vérifier le nombre exact de tâches (si connu)
        self.assertEqual(Task.objects.count(), 3, "Le nombre de tâches importées est incorrect")
