from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    fieldsets = UserAdmin.fieldsets + (("Información adicional", {"fields": ("telefono", "fotografia")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Información personal", {"fields": ("first_name", "last_name", "email", "telefono", "fotografia")}),)
