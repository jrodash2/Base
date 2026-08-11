from django.urls import path
from . import views

app_name = "usuarios"
urlpatterns = [
    path("", views.UsuarioListaView.as_view(), name="lista"),
    path("nuevo/", views.UsuarioCrearView.as_view(), name="crear"),
    path("perfil/", views.PerfilView.as_view(), name="perfil"),
    path("<int:pk>/", views.UsuarioDetalleView.as_view(), name="detalle"),
    path("<int:pk>/editar/", views.UsuarioEditarView.as_view(), name="editar"),
    path("<int:pk>/estado/", views.cambiar_estado, name="estado"),
    path("<int:pk>/clave/", views.RestablecerClaveView.as_view(), name="clave"),
]
