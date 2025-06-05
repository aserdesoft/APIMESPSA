from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from api.Models.ProductoServicioModels import *
from api.Serializers.ProductoServicioSerializers import *
from api.utils import ArticuloPagination
from api.utils import FiltroArticulo,FiltroCategoria
class UnidadViewset(ModelViewSet):
    queryset = Unidad.objects.all().order_by("claveUnidad")
    serializer_class = UnidadSerializer
    """ 
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    """

class CategoriaViewset(ModelViewSet):
    queryset = Categoria.objects.all().order_by("nombre")
    serializer_class = CategoriaSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FiltroCategoria
    """ 
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    """

class ProductosViewset(ModelViewSet):
    queryset = Articulo.objects.filter(tipoArticulo=TipoArticulo.PRODUCTO).order_by("nombre")
    pagination_class = ArticuloPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FiltroArticulo
    """ 
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    """
    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return ArticuloSerializadorInterno
        elif self.action == 'retrieve':
            return ArticuloSerializadorIndExterno
        return ArticuloSerializadorListaExterno
            

class ServiciosViewset(ModelViewSet):
    queryset = Articulo.objects.filter(tipoArticulo=TipoArticulo.SERVICIO).order_by("nombre")
    pagination_class = ArticuloPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FiltroArticulo
    """
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    """
    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return ArticuloSerializadorInterno
        elif self.action == 'retrieve':
            return ArticuloSerializadorIndExterno
        return ArticuloSerializadorListaExterno

class ImagenViewSet(ModelViewSet):
    queryset = Imagen.objects.all()
    @action(detail=False, methods=['post'])
    def subir_multiples(self, request):
        archivos = request.FILES.getlist('archivos')
        articulo_id = request.data.get('articulo')

        if not archivos or not articulo_id:
            return Response({'error': 'Debes proporcionar archivos y el ID del artículo'}, status=status.HTTP_400_BAD_REQUEST)

        imagenes_creadas = []
        for archivo in archivos:
            imagen = Imagen(archivo=archivo, articulo_id=articulo_id)
            imagen.save()
            imagenes_creadas.append(imagen)

        serializer = self.get_serializer(imagenes_creadas, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    """
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    """
    def get_serializer_class(self):
        #user = self.request.user
        #if user.is_staff or user.is_superuser:
        return ImagenSerializerInterno
        #return ImagenSerializerExterno
    