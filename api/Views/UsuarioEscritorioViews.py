from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from api.Serializers.UsuarioEscritorioSerializers import *
from api.Serializers.UsuarioSerializers import *
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

class PerfilUsuario(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            perfil = request.user.perfil  # OneToOneField en Usuario
            serializer = ActualizarDatos(perfil)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Perfil.DoesNotExist:
            return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        try:
            perfil = request.user.perfil
        except Perfil.DoesNotExist:
            return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ActualizarDatos(perfil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditarUsuarioPorCorreoView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request):
        correo = request.data.get("correoElectronico")
        if not correo:
            return Response({"error": "Se requiere el correo electrónico."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(correoElectronico=correo)
            perfil = usuario.perfil
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado con ese correo"}, status=status.HTTP_404_NOT_FOUND)
        except Perfil.DoesNotExist:
            return Response({"error": "Perfil no encontrado para ese usuario"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ActualizarDatos(perfil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
