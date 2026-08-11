from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    email = models.EmailField("correo electrónico", unique=True)
    telefono = models.CharField("teléfono", max_length=30, blank=True)
    fotografia = models.ImageField("fotografía", upload_to="usuarios/", blank=True, null=True)

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        permissions = [
            ("activate_usuario", "Puede activar o desactivar usuarios"),
            ("assign_roles", "Puede cambiar roles de usuarios"),
            ("reset_usuario_password", "Puede restablecer contraseñas de usuarios"),
            ("access_dashboard", "Puede acceder al dashboard administrativo"),
        ]

    @property
    def nombre_completo(self):
        return self.get_full_name() or self.username

    @property
    def roles(self):
        return ", ".join(self.groups.values_list("name", flat=True)) or "Sin rol"
