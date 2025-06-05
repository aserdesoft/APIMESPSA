from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from api.Views.FiscalViews import *
from api.Views.UsuarioViews import *
from api.Views.UsuarioEscritorioViews import *
from api.Views.ProductoServicioViews import *
from api.Views.EmailViews import *
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
    path("send-reset-code/", send_reset_code, name="send-reset-code"),
    path("verify-reset-code/", verify_reset_code, name="verify-reset-code"),
    path("personas/",ObtenerPersonasView.as_view()),
    path("login-winforms/", LoginWinFormsView.as_view(), name="login-winforms"),
    path("listar-usuarios/", ListarUsuariosView.as_view(), name="listar-usuarios"),
    path('editar-usuario-correo/', EditarUsuarioPorCorreoView.as_view(), name='editar-usuario-correo'),
]