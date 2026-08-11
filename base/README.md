# Plantilla base Django + Riho

Base reutilizable en español para proyectos Django. Integra los recursos existentes de Riho directamente desde `../Riho/assets` (no los duplica), usuario personalizado, autenticación, dashboard y administración de usuarios mediante permisos nativos.

## Requisitos

- Python 3.10 o posterior.
- PostgreSQL es opcional; SQLite funciona sin configuración adicional.

## Instalación en Windows (PowerShell)

```powershell
cd base
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py configurar_sistema
python manage.py runserver
```

`configurar_sistema` crea o actualiza de forma idempotente el grupo **Administrador**, le asigna los permisos de usuarios y, si aún no existe, solicita interactivamente los datos del primer superusuario. También se puede omitir esa pregunta con `python manage.py configurar_sistema --sin-superusuario` y ejecutar después `python manage.py createsuperuser`.

## Instalación en Linux/macOS

```bash
cd base
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py configurar_sistema
python manage.py runserver
```

Abra `http://127.0.0.1:8000/`. El admin técnico para superusuarios permanece en `http://127.0.0.1:8000/admin/`.

## Configuración

Nunca confirme `.env`. Para desarrollo, `DB_ENGINE=sqlite` crea `db.sqlite3`. Para PostgreSQL use `DB_ENGINE=postgresql` y complete `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` y `DB_PORT`. El correo sale por consola de forma predeterminada; para producción configure las variables SMTP incluidas en `.env.example`.

Los archivos subidos se guardan en `media/`. Los recursos originales de Riho siguen en `Riho/assets`; `STATICFILES_DIRS` los expone sin realizar una copia. En despliegue ejecute:

```bash
python manage.py collectstatic --noinput
```

## Pruebas y verificaciones

```bash
python manage.py check
python manage.py makemigrations --check
python manage.py test
python manage.py collectstatic --noinput
```

## Extender la plantilla

1. Cree la aplicación: `python manage.py startapp inventario`.
2. Añádala a `INSTALLED_APPS` y conecte sus URL con un `namespace`.
3. Extienda `{% extends 'layouts/base.html' %}` en cada página.
4. Complete `title`, `page_title`, `breadcrumbs`, `content`, `extra_css` y `extra_js` según corresponda.
5. Cree permisos en `Meta.permissions` del modelo o use los permisos automáticos `view`, `add`, `change` y `delete`.
6. Proteja las vistas con `LoginRequiredMixin` y `PermissionRequiredMixin` (o sus decoradores equivalentes).
7. Agregue la opción en `templates/includes/sidebar.html` dentro de `{% if perms.aplicacion.codename %}` para que solo sea visible a quien tenga acceso.
8. Asigne el permiso a los grupos necesarios desde Django Admin o desde una migración/orden idempotente.

El cierre de sesión se implementa deliberadamente con un formulario `POST` y token CSRF. La desactivación sustituye a la eliminación física como acción principal para preservar trazabilidad.
