from django.test import TestCase
from django.urls import reverse
from .models import Task
import os
from django.core.management import call_command
from .utils import tc


class TaskModelTest(TestCase):

    @tc("TA00")  # Test hors plan YAML
    def test_str_returns_title(self):
        task = Task(title="My task")
        self.assertEqual(str(task), "My task")


class TaskViewsTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Demo task")

    @tc("TA01")  # Test d'accès à la page liste
    def test_homepage_renders(self):
        response = self.client.get(reverse("list"))
        self.assertEqual(response.status_code, 200)

    @tc("TA02")  # Création d’une tâche
    def test_create_task_via_post(self):
        response = self.client.post(reverse("list"), {"title": "New task"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="New task").exists())

    @tc("TA04")  # Affichage page d’édition
    def test_update_page_renders(self):
        response = self.client.get(reverse("update_task", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    @tc("TA05")  # Modification d’une tâche
    def test_update_task_via_post(self):
        response = self.client.post(
            reverse("update_task", args=[self.task.id]),
            {"title": "Updated title"},
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated title")

    @tc("TA06")  # Affichage page suppression
    def test_delete_page_renders(self):
        response = self.client.get(reverse("delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    @tc("TA07")  # Suppression d’une tâche
    def test_delete_task_via_post(self):
        response = self.client.post(reverse("delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


class EntryPointModulesTest(TestCase):

    @tc("TA08")  # Import WSGI
    def test_wsgi_module_imports(self):
        from todo import wsgi
        self.assertIsNotNone(wsgi.application)

    @tc("TA09")  # Import ASGI
    def test_asgi_module_imports(self):
        from todo import asgi
        self.assertIsNotNone(asgi.application)


class FixturesTest(TestCase):

    @tc("TA10")  # Import JSON
    def test_fixture_import(self):
        """Teste l'import du fichier JSON et vérifie que les tâches sont en base"""

        fixture_path = os.path.join(
            os.path.dirname(__file__),
            'fixtures',
            'dataset.json'
        )

        call_command('loaddata', fixture_path, verbosity=0)

        self.assertTrue(Task.objects.exists(), "Aucune tâche n'a été importée")

        self.assertTrue(
            Task.objects.filter(title="Buy groceries").exists(),
            "La tâche 'Buy groceries' n'a pas été importée"
        )

        self.assertEqual(Task.objects.count(), 3, "Le nombre de tâches importées est incorrect")
