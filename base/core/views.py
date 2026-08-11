from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from usuarios.models import Usuario


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm("usuarios.access_dashboard"):
            users = Usuario.objects.all()
            context.update(total_usuarios=users.count(), usuarios_activos=users.filter(is_active=True).count(),
                           usuarios_inactivos=users.filter(is_active=False).count(),
                           ultimos_usuarios=users.prefetch_related("groups").order_by("-date_joined")[:5])
        return context


def error_403(request, exception=None):
    return render(request, "core/403.html", status=403)

def error_404(request, exception=None):
    return render(request, "core/404.html", status=404)

def error_500(request):
    return render(request, "core/500.html", status=500)
