from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import *
from .views import UsuarioEditarPorCorreoAPIView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('CFDI',UsoCFDIViewset,'usocfdi')
router.register('passwords',PasswordCuentaEspecialViewset,'passwords')
router.register('unidades',UnidadViewset,'unidades')
router.register('categorias',CategoriaViewset,'categorias')
router.register('productos',ProductosViewset,'productos')
router.register('servicios',ServiciosViewset,'servicios')
router.register('imagenes', ImagenViewSet,'imagenes')
urlpatterns = [
    path('',include(router.urls)),
    path("token/",obtenerParTokenView.as_view()),
    path("token/refresh/",TokenRefreshView.as_view()),
    path("registrar/",RegistrarView.as_view()),
    path("combinaciones/", ObtenerCuentasView.as_view()),
    path("validarCuentaEsp/",ValidarCuentaEspecialView.as_view()),
    path("dashboard/perfil/", PerfilUsuarioAPIView.as_view(), name="perfil-usuario"),
    path('usuarios/activar/', CambiarEstadoUsuarioView.as_view(), name='cambiar-estado-usuario'),
    path("personas/",ObtenerPersonasView.as_view()),
    path("login-winforms/", LoginWinFormsView.as_view(), name="login-winforms"),
    path("listar-usuarios/", ListarUsuariosView.as_view(), name="listar-usuarios"),
    path('api/usuarios/editar-usuario-por-correo/<str:correo>/', UsuarioEditarPorCorreoAPIView.as_view()),
]