from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.response import Response
from rest_framework import generics, status
from api.Serializers.UsuarioSerializers import *
from api.utils import TipoCuenta
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from .serializers import UsuarioSerializer
from urllib.parse import unquote
from django.shortcuts import get_object_or_404
class UsoCFDIViewset(ModelViewSet):
    queryset = UsoCFDI.objects.all().order_by("usoCFDI")
    permission_classes = [IsAuthenticated]
    serializer_class = UsoCFDISerializer

class PasswordCuentaEspecialViewset(ModelViewSet):
    queryset = PasswordCuentaEspecial.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = PasswordCuentaEspecialSerializador

class obtenerParTokenView(TokenObtainPairView):
    serializer_class= serializadorObtenerParToken
    permission_classes = (AllowAny, )
    '''
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get("access")
        refresh_token = response.data.get("refresh")
        if refresh_token and access_token:
            del response.data["refresh"]
            del response.data["access"]
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,        # Usa HTTPS en producción
                samesite="Lax",     # Ajusta según tus necesidades
                max_age=7 * 24 * 60 * 60,
                path="/api/token/refresh/",  # Donde se usará
            )
            response.set_cookie(
                key="access_token",
                value=refresh_token,
                httponly=True,
                secure=True,        # Usa HTTPS en producción
                samesite="Lax",     # Ajusta según tus necesidades
                max_age=7 * 24 * 60 * 60,
                path="/api/token/refresh/",  # Donde se usará
            )

        return response
    '''

class RegistrarView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = RegistrarSerializador

class ObtenerCuentasView(generics.RetrieveAPIView):
    permission_classes = (AllowAny, )
    def get(self,request=None):
        # Obtenemos las combinaciones de la clase TipoCuenta
        combinaciones = TipoCuenta.combinaciones()
        # Devolvemos la respuesta con Response, especificando el formato JSON
        return Response({"combinaciones": combinaciones})

class ObtenerPersonasView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,IsAuthenticated)
    def get(self,request=None):
        # Obtenemos las combinaciones de la clase TipoCuenta
        personas = TipoCuenta.personas()
        # Devolvemos la respuesta con Response, especificando el formato JSON
        return Response({"TP": personas})

class PerfilUsuarioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            perfil = request.user.perfil  # OneToOneField en Usuario
            serializer = PerfilDashboardSerializador(perfil)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Perfil.DoesNotExist:
            return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        try:
            perfil = request.user.perfil
        except Perfil.DoesNotExist:
            return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PerfilDashboardSerializador(perfil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CambiarEstadoUsuarioView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request):
        correo = request.data.get("correoElectronico")
        if not correo:
            return Response("El campo de correo electronico es requerido.", status=status.HTTP_400_BAD_REQUEST)
        try:
            usuario = Usuario.objects.get(correoElectronico=correo)
        except Usuario.DoesNotExist:
            return Response("Usuario no encontrado con ese correo.", status=status.HTTP_404_NOT_FOUND)
        # Verificación de permisos
        if request.user != usuario and not (request.user.is_staff or request.user.is_superuser):
            return Response("No puedes modificar el estado de otro usuario.", status=status.HTTP_403_FORBIDDEN)

        serializer = UsuarioIsActiveSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ValidarCuentaEspecialView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ValidarCuentaEspecialSerializador

    def post(self, request, *args, **kwargs):
        # Crear el serializador y pasar los datos
        serializer = ValidarCuentaEspecialSerializador(data=request.data)

        if serializer.is_valid():
            # Si la validación pasa, obtener el objeto validado
            objElim = serializer.validated_data["obj_validado"]
            # Eliminar la cuenta validada
            objElim.delete()
            return Response({"mensaje": "OK"}, status=status.HTTP_200_OK)

        return Response({"mensaje": "ERROR", "detalles": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#Vista para el login desde la app de escritorio
class LoginWinFormsView(APIView):
    def post(self, request):
        serializer = ValidarUsuarioSimpleSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"resultado": "OK"}, status=status.HTTP_200_OK)
        return Response({"resultado": "ERROR"}, status=status.HTTP_401_UNAUTHORIZED)
    

class ListarUsuariosView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PerfilDashboardSerializador

    def get_queryset(self):
        queryset = Perfil.objects.all()
        tipo_cuenta = self.request.query_params.get('tipoCuenta', None)
        if tipo_cuenta is not None:
            queryset = queryset.filter(tipoCuenta=tipo_cuenta)
        return queryset
class EditarUsuarioPorCorreoView(APIView):
    def patch(self, request, correo):
        correo = unquote(correo)  # Decodifica %40 a @

        try:
            usuario = Usuario.objects.get(correo_electronico=correo)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)