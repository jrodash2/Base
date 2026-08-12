from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from usuarios.forms import FormularioAutenticacion
from configuracion.models import ConfiguracionSistema


class RecuperacionInstitucionalView(auth_views.PasswordResetView):
    template_name = "registration/password_reset_form.html"
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"

    def form_valid(self, form):
        self.extra_email_context = {"configuracion_sistema": ConfiguracionSistema.obtener()}
        return super().form_valid(form)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Keep Django's password-management routes, then declare the branded login
    # afterwards so that reverse("login") resolves to the Riho view rather than
    # the login route bundled by django.contrib.auth.urls.
    path("cuenta/password_reset/", RecuperacionInstitucionalView.as_view(), name="password_reset"),
    path("cuenta/", include("django.contrib.auth.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html", authentication_form=FormularioAutenticacion), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("usuarios/", include("usuarios.urls")),
    path("configuracion/", include("configuracion.urls")),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "core.views.error_403"
handler404 = "core.views.error_404"
handler500 = "core.views.error_500"
