from django.test import TestCase
from django.urls import reverse
from usuarios.models import Usuario

class DashboardTests(TestCase):
    def test_requiere_autenticacion(self):
        self.assertRedirects(self.client.get(reverse("dashboard")), f'{reverse("login")}?next=/')

    def test_usuario_autenticado_accede(self):
        user = Usuario.objects.create_user("ana", password="Clave-Segura-123")
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 200)
