from django import forms

from .models import ConfiguracionSistema


class ConfiguracionSistemaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionSistema
        exclude = ("actualizado_por",)
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "color_primario": forms.TextInput(attrs={"type": "color"}),
            "color_secundario": forms.TextInput(attrs={"type": "color"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs.update({"class": "form-control image-input", "accept": ".png,.jpg,.jpeg,.webp,.gif"})
            else:
                field.widget.attrs["class"] = "form-control"
