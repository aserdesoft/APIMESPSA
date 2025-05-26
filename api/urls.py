from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('usuarios', UsuarioViewSet, basename='usuario') 
router.register('CFDI',UsoCFDIViewset,'usocfdi')
router.register('passwords',PasswordCuentaEspecialViewset,'passwords')

urlpatterns = [
    path('',include(router.urls)),
    path("token/",obtenerParTokenView.as_view()),
    path("token/refresh/",TokenRefreshView.as_view()),
    path("registrar/",RegistrarView.as_view()),
    path("combinaciones/", ObtenerCuentasView.as_view()),
    path("validarCuentaEsp/",ValidarCuentaEspecialView.as_view()),
    path("dashboard/perfil/", PerfilUsuarioAPIView.as_view(), name="perfil-usuario"),
    path("personas/",ObtenerPersonasView.as_view()),
    path("login-winforms/", LoginWinFormsView.as_view(), name="login-winforms"),
    path("listar-usuarios/", ListarUsuariosView.as_view(), name="listar-usuarios"),
   
]