from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from .forms import ConfiguracionSistemaForm
from .models import ConfiguracionSistema


@login_required
def general(request):
    puede_editar = request.user.is_superuser or request.user.has_perm("configuracion.change_configuracionsistema")
    puede_ver = puede_editar or request.user.has_perm("configuracion.view_configuracionsistema")
    if not puede_ver:
        raise PermissionDenied
    if request.method == "POST" and not puede_editar:
        raise PermissionDenied
    configuracion = ConfiguracionSistema.obtener(crear=True)
    if request.method == "POST":
        form = ConfiguracionSistemaForm(request.POST, request.FILES, instance=configuracion)
        if form.is_valid():
            objeto = form.save(commit=False)
            objeto.actualizado_por = request.user
            objeto.save()
            messages.success(request, "La configuración institucional se actualizó correctamente.")
            return redirect("configuracion:general")
        messages.error(request, "Revise los campos marcados antes de guardar.")
    else:
        form = ConfiguracionSistemaForm(instance=configuracion)
    return render(request, "configuracion/general.html", {"form": form, "configuracion": configuracion, "puede_editar": puede_editar})
