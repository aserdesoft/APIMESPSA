from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics,status
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

class UsuarioEditarPorCorreoAPIView(APIView):
    def patch(self, request, correo):
        try:
            usuario = Usuario.objects.get(correoElectronico=correo)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)