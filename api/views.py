from api.models import Usuario, UsoCFDI,PasswordCuentaEspecial
from api.serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.response import Response
from api.utils import TipoCuenta
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

class UsoCFDIViewset(ModelViewSet):
    queryset = UsoCFDI.objects.all().order_by("usoCFDI")
    permission_classes = [AllowAny]
    serializer_class = UsoCFDISerializer

class PasswordCuentaEspecialViewset(ModelViewSet):
    queryset = PasswordCuentaEspecial.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PasswordCuentaEspecialSerializador

class obtenerParTokenView(TokenObtainPairView):
    serializer_class= serializadorObtenerParToken
    permission_classes = (AllowAny, )

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
    permission_classes = (AllowAny, )
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
