import shutil
import tempfile
from io import StringIO

from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from usuarios.models import Usuario
from .context_processors import configuracion_sistema
from .models import ConfiguracionSistema


MEDIA_ROOT = tempfile.mkdtemp()
GIF = b"GIF87a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ConfiguracionSistemaTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.admin = Usuario.objects.create_user("admin-config", email="admin-config@example.com", password="Clave-Segura-123")
        self.normal = Usuario.objects.create_user("normal-config", email="normal-config@example.com", password="Clave-Segura-123")
        permissions = Permission.objects.filter(codename__in=("view_configuracionsistema", "change_configuracionsistema"))
        self.admin.user_permissions.set(permissions)

    def test_singleton_reutiliza_unico_registro(self):
        primero = ConfiguracionSistema.obtener(crear=True)
        segundo = ConfiguracionSistema(nombre_institucion="Institución reemplazada")
        with self.assertRaises(ValidationError):
            segundo.save()
        self.assertEqual(ConfiguracionSistema.objects.count(), 1)
        self.assertEqual(ConfiguracionSistema.obtener().pk, primero.pk)

    def test_administrador_abre_vista(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse("configuracion:general")).status_code, 200)

    def test_usuario_sin_permiso_recibe_403_y_no_ve_enlace(self):
        self.client.force_login(self.normal)
        self.assertEqual(self.client.get(reverse("configuracion:general")).status_code, 403)
        self.assertNotContains(self.client.get(reverse("dashboard")), "Configuración general")

    def test_guarda_datos_y_logos(self):
        self.client.force_login(self.admin)
        data = {
            "nombre_institucion": "Instituto de Pruebas", "nombre_corto": "Instituto", "siglas": "IP",
            "slogan": "Calidad", "descripcion": "Descripción", "direccion": "Calle 1", "telefono": "123",
            "telefono_secundario": "456", "correo": "info@example.com", "sitio_web": "https://example.com",
            "nit": "123-4", "horario_atencion": "8 a 5", "nombre_sistema": "Gestión IP",
            "version_sistema": "1.0", "texto_pie_pagina": "Todos los derechos reservados",
            "color_primario": "#112233", "color_secundario": "#AABBCC",
            "logo_primario": SimpleUploadedFile("primario.gif", GIF, content_type="image/gif"),
            "logo_secundario": SimpleUploadedFile("secundario.gif", GIF, content_type="image/gif"),
        }
        response = self.client.post(reverse("configuracion:general"), data)
        self.assertRedirects(response, reverse("configuracion:general"))
        config = ConfiguracionSistema.obtener()
        self.assertEqual(config.nombre_institucion, "Instituto de Pruebas")
        self.assertEqual(config.actualizado_por, self.admin)
        self.assertTrue(config.logo_primario.name)
        self.assertTrue(config.logo_secundario.name)

    def test_contexto_y_layout_sin_configuracion_previa(self):
        self.assertIsNone(configuracion_sistema(None)["configuracion_sistema"])
        self.client.force_login(self.normal)
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 200)

    def test_datos_institucionales_y_customizer_en_layout(self):
        ConfiguracionSistema.objects.create(nombre_institucion="Academia Central", nombre_sistema="Portal Central")
        self.client.force_login(self.normal)
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, "Academia Central")
        self.assertContains(response, "Portal Central")
        self.assertContains(response, 'class="customizer-links"')

    def test_comando_es_idempotente(self):
        call_command("configurar_sistema", "--sin-superusuario", stdout=StringIO())
        call_command("configurar_sistema", "--sin-superusuario", stdout=StringIO())
        self.assertEqual(ConfiguracionSistema.objects.count(), 1)
