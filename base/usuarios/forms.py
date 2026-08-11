from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from .models import Usuario

class EstiloRihoMixin:
    def aplicar_estilos(self):
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-control"

class FormularioAutenticacion(EstiloRihoMixin, AuthenticationForm):
    error_messages = {"invalid_login": "El usuario o la contraseña son incorrectos.", "inactive": "Esta cuenta está inactiva."}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs); self.aplicar_estilos()

class UsuarioCreacionForm(EstiloRihoMixin, UserCreationForm):
    groups = forms.ModelMultipleChoiceField(Group.objects.all(), required=False, label="Roles", widget=forms.SelectMultiple(attrs={"class": "form-select"}))
    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "telefono", "fotografia", "groups", "is_active")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs); self.aplicar_estilos()

class UsuarioEdicionForm(EstiloRihoMixin, UserChangeForm):
    password = None
    groups = forms.ModelMultipleChoiceField(Group.objects.all(), required=False, label="Roles", widget=forms.SelectMultiple(attrs={"class": "form-select"}))
    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "telefono", "fotografia", "groups", "is_active")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs); self.aplicar_estilos()
    def clean(self):
        data = super().clean()
        if self.instance == getattr(self, "actor", None) and not data.get("is_active"):
            self.add_error("is_active", "No puede desactivar su propia cuenta.")
        admin = Group.objects.filter(name="Administrador").first()
        if admin and admin in self.instance.groups.all() and admin not in data.get("groups", []) and not Usuario.objects.filter(groups=admin, is_active=True).exclude(pk=self.instance.pk).exists():
            self.add_error("groups", "No puede quitar el rol al único administrador activo.")
        return data

class PerfilForm(EstiloRihoMixin, forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ("first_name", "last_name", "email", "telefono", "fotografia")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs); self.aplicar_estilos()

class CambioClaveForm(EstiloRihoMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs); self.aplicar_estilos()

class RestablecerClaveForm(EstiloRihoMixin, forms.Form):
    nueva_clave1 = forms.CharField(label="Nueva contraseña", widget=forms.PasswordInput)
    nueva_clave2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)
    def __init__(self, usuario, *args, **kwargs):
        self.usuario = usuario; super().__init__(*args, **kwargs); self.aplicar_estilos()
    def clean(self):
        from django.contrib.auth.password_validation import validate_password
        data = super().clean()
        if data.get("nueva_clave1") != data.get("nueva_clave2"):
            self.add_error("nueva_clave2", "Las contraseñas no coinciden.")
        elif data.get("nueva_clave1"):
            validate_password(data["nueva_clave1"], self.usuario)
        return data
