from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView

from .forms import PerfilForm, RestablecerClaveForm, UsuarioCreacionForm, UsuarioEdicionForm
from .models import Usuario

class MensajeExitoMixin:
    mensaje_exito = "Operación realizada correctamente."
    def form_valid(self, form):
        messages.success(self.request, self.mensaje_exito)
        return super().form_valid(form)

class UsuarioListaView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Usuario; template_name = "usuarios/lista.html"; context_object_name = "usuarios"; paginate_by = 10
    permission_required = "usuarios.view_usuario"; raise_exception = True
    def get_queryset(self):
        qs = Usuario.objects.prefetch_related("groups").order_by("username")
        q = self.request.GET.get("q", "").strip()
        return qs.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q)) if q else qs

class UsuarioCrearView(LoginRequiredMixin, PermissionRequiredMixin, MensajeExitoMixin, CreateView):
    model = Usuario; form_class = UsuarioCreacionForm; template_name = "usuarios/formulario.html"
    permission_required = "usuarios.add_usuario"; raise_exception = True; success_url = reverse_lazy("usuarios:lista"); mensaje_exito = "Usuario creado correctamente."
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.has_perm("usuarios.assign_roles"):
            form.fields.pop("groups", None)
        return form

class UsuarioDetalleView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Usuario; template_name = "usuarios/detalle.html"; context_object_name = "usuario"
    permission_required = "usuarios.view_usuario"; raise_exception = True
    def get_queryset(self): return Usuario.objects.prefetch_related("groups")

class UsuarioEditarView(LoginRequiredMixin, PermissionRequiredMixin, MensajeExitoMixin, UpdateView):
    model = Usuario; form_class = UsuarioEdicionForm; template_name = "usuarios/formulario.html"
    permission_required = "usuarios.change_usuario"; raise_exception = True; success_url = reverse_lazy("usuarios:lista"); mensaje_exito = "Usuario actualizado correctamente."
    def get_form(self, form_class=None):
        form = super().get_form(form_class); form.actor = self.request.user
        if not self.request.user.has_perm("usuarios.assign_roles"):
            form.fields.pop("groups", None)
        return form

@login_required
@permission_required("usuarios.activate_usuario", raise_exception=True)
def cambiar_estado(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method != "POST":
        return redirect("usuarios:detalle", pk=pk)
    if usuario == request.user:
        messages.error(request, "No puede desactivar su propia cuenta.")
    else:
        usuario.is_active = not usuario.is_active; usuario.save(update_fields=["is_active"])
        messages.success(request, "Estado del usuario actualizado.")
    return redirect("usuarios:detalle", pk=pk)

class RestablecerClaveView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "usuarios/clave.html"; permission_required = "usuarios.reset_usuario_password"; raise_exception = True
    def dispatch(self, request, *args, **kwargs):
        self.usuario = get_object_or_404(Usuario, pk=kwargs["pk"]); return super().dispatch(request, *args, **kwargs)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs(); kwargs["usuario"] = self.usuario; return kwargs
    form_class = RestablecerClaveForm
    def form_valid(self, form):
        self.usuario.set_password(form.cleaned_data["nueva_clave1"]); self.usuario.save(update_fields=["password"])
        messages.success(self.request, "Contraseña restablecida correctamente."); return redirect("usuarios:detalle", pk=self.usuario.pk)

class PerfilView(LoginRequiredMixin, MensajeExitoMixin, UpdateView):
    form_class = PerfilForm; template_name = "usuarios/perfil.html"; success_url = reverse_lazy("usuarios:perfil"); mensaje_exito = "Perfil actualizado correctamente."
    def get_object(self, queryset=None): return self.request.user
