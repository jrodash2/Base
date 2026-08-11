from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand, call_command

class Command(BaseCommand):
    help = "Crea el rol Administrador y opcionalmente el primer superusuario."
    def add_arguments(self, parser):
        parser.add_argument("--sin-superusuario", action="store_true", help="No solicitar la creación del superusuario")
    def handle(self, *args, **options):
        permisos = Permission.objects.filter(content_type__app_label="usuarios")
        grupo, creado = Group.objects.get_or_create(name="Administrador")
        grupo.permissions.set(permisos)
        self.stdout.write(self.style.SUCCESS(f"Grupo Administrador {'creado' if creado else 'actualizado'} con {permisos.count()} permisos."))
        from usuarios.models import Usuario
        if not options["sin_superusuario"] and not Usuario.objects.filter(is_superuser=True).exists():
            self.stdout.write("No existe un superusuario. Complete los datos solicitados.")
            call_command("createsuperuser")
