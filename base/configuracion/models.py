from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models

MAX_IMAGE_SIZE = 5 * 1024 * 1024
color_validator = RegexValidator(r"^#[0-9A-Fa-f]{6}$", "Ingrese un color hexadecimal válido, por ejemplo #006666.")
extension_validator = FileExtensionValidator(["png", "jpg", "jpeg", "webp", "gif"])


def validar_tamano_imagen(archivo):
    if archivo.size > MAX_IMAGE_SIZE:
        raise ValidationError("La imagen no puede superar 5 MB.")


def ruta_identidad(instance, filename):
    return f"configuracion/identidad/{Path(filename).name}"


class ConfiguracionSistema(models.Model):
    nombre_institucion = models.CharField("nombre de la institución", max_length=200)
    nombre_corto = models.CharField("nombre corto", max_length=100, blank=True)
    siglas = models.CharField("siglas", max_length=30, blank=True)
    slogan = models.CharField("eslogan", max_length=250, blank=True)
    descripcion = models.TextField("descripción", blank=True)
    logo_primario = models.ImageField("logo primario", upload_to=ruta_identidad, blank=True, validators=[extension_validator, validar_tamano_imagen])
    logo_secundario = models.ImageField("logo secundario", upload_to=ruta_identidad, blank=True, validators=[extension_validator, validar_tamano_imagen])
    favicon = models.ImageField("favicon", upload_to=ruta_identidad, blank=True, validators=[extension_validator, validar_tamano_imagen])
    direccion = models.CharField("dirección", max_length=250, blank=True)
    telefono = models.CharField("teléfono", max_length=30, blank=True)
    telefono_secundario = models.CharField("teléfono secundario", max_length=30, blank=True)
    correo = models.EmailField("correo electrónico", blank=True)
    sitio_web = models.URLField("sitio web", blank=True)
    nit = models.CharField("NIT", max_length=50, blank=True)
    horario_atencion = models.CharField("horario de atención", max_length=150, blank=True)
    nombre_sistema = models.CharField("nombre del sistema", max_length=150, default="Sistema base")
    version_sistema = models.CharField("versión del sistema", max_length=30, blank=True)
    texto_pie_pagina = models.CharField("texto del pie de página", max_length=250, blank=True)
    color_primario = models.CharField("color primario", max_length=7, default="#006666", validators=[color_validator])
    color_secundario = models.CharField("color secundario", max_length=7, default="#FF6150", validators=[color_validator])
    fecha_actualizacion = models.DateTimeField("fecha de actualización", auto_now=True)
    actualizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="actualizado por", null=True, blank=True, on_delete=models.SET_NULL, related_name="configuraciones_actualizadas")

    class Meta:
        verbose_name = "configuración del sistema"
        verbose_name_plural = "configuración del sistema"

    def save(self, *args, **kwargs):
        self.pk = 1
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_institucion

    @classmethod
    def obtener(cls, crear=False):
        if crear:
            obj, _ = cls.objects.get_or_create(pk=1, defaults={"nombre_institucion": "Mi institución"})
            return obj
        return cls.objects.filter(pk=1).first()
