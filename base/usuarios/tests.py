from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse
from .models import Usuario

CLAVE = "Clave-Segura-123"
class AutenticacionTests(TestCase):
    def setUp(self): self.user = Usuario.objects.create_user("ana", "ana@example.com", CLAVE)
    def test_login_correcto(self):
        self.assertRedirects(self.client.post(reverse("login"), {"username": "ana", "password": CLAVE}), reverse("dashboard"))
    def test_login_incorrecto(self):
        response = self.client.post(reverse("login"), {"username": "ana", "password": "mala"})
        self.assertContains(response, "incorrectos")
    def test_logout_solo_post(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertRedirects(self.client.post(reverse("logout")), reverse("login"))

class AdministracionTests(TestCase):
    def setUp(self):
        self.admin = Usuario.objects.create_user("admin", "admin@example.com", CLAVE)
        permisos = Permission.objects.filter(content_type__app_label="usuarios")
        self.admin.user_permissions.set(permisos)
        self.normal = Usuario.objects.create_user("normal", "normal@example.com", CLAVE)
    def test_admin_accede_lista(self):
        self.client.force_login(self.admin); self.assertEqual(self.client.get(reverse("usuarios:lista")).status_code, 200)
    def test_sin_permisos_denegado(self):
        self.client.force_login(self.normal); self.assertEqual(self.client.get(reverse("usuarios:lista")).status_code, 403)
    def test_crear_usuario_y_asignar_grupo(self):
        grupo = Group.objects.create(name="Editor"); self.client.force_login(self.admin)
        data = {"username":"nuevo", "email":"nuevo@example.com", "password1":CLAVE, "password2":CLAVE, "groups":[grupo.pk], "is_active":"on"}
        self.assertRedirects(self.client.post(reverse("usuarios:crear"), data), reverse("usuarios:lista"))
        self.assertTrue(Usuario.objects.get(username="nuevo").groups.filter(pk=grupo.pk).exists())
    def test_activar_desactivar(self):
        self.client.force_login(self.admin); url = reverse("usuarios:estado", args=[self.normal.pk])
        self.client.post(url); self.normal.refresh_from_db(); self.assertFalse(self.normal.is_active)
        self.client.post(url); self.normal.refresh_from_db(); self.assertTrue(self.normal.is_active)
    def test_cambio_clave_propia_conserva_sesion(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse("password_change"), {"old_password":CLAVE, "new_password1":"Otra-Clave-456!", "new_password2":"Otra-Clave-456!"})
        self.assertRedirects(response, reverse("password_change_done")); self.assertIn("_auth_user_id", self.client.session)
