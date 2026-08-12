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

    def test_dashboard_incluye_configurador_riho(self):
        user = Usuario.objects.create_user("tema", password="Clave-Segura-123")
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, 'class="customizer-links"')
        self.assertContains(response, 'class="customizer-contain"')
        self.assertContains(response, "js/theme-customizer/customizer.js")
        for image_number in range(1, 6):
            self.assertContains(response, f"images/customizer/{image_number}.png")

    def test_login_no_incluye_configurador(self):
        response = self.client.get(reverse("login"))
        self.assertNotContains(response, 'class="customizer-links"')
        self.assertNotContains(response, "js/theme-customizer/customizer.js")
