from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from usuarios.forms import FormularioAutenticacion

urlpatterns = [
    path("admin/", admin.site.urls),
    # Keep Django's password-management routes, then declare the branded login
    # afterwards so that reverse("login") resolves to the Riho view rather than
    # the login route bundled by django.contrib.auth.urls.
    path("cuenta/", include("django.contrib.auth.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html", authentication_form=FormularioAutenticacion), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("usuarios/", include("usuarios.urls")),
    path("", include("core.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "core.views.error_403"
handler404 = "core.views.error_404"
handler500 = "core.views.error_500"
