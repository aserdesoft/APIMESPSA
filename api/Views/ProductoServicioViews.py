from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from api.Models.ProductoServicioModels import *
from api.Serializers.ProductoServicioSerializers import *
from api.utils import ArticuloPagination
class UnidadViewset(ModelViewSet):
    queryset = Unidad.objects.all().order_by("claveUnidad")
    serializer_class = UnidadSerializer
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated()]

class CategoriaViewset(ModelViewSet):
    queryset = Categoria.objects.all().order_by("nombre")
    serializer_class = CategoriaSerializer
    pagination_class = ArticuloPagination
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated()]
class ProductosViewset(ModelViewSet):
    queryset = Articulo.objects.filter(tipoArticulo="PDT").order_by("nombre")
    pagination_class = ArticuloPagination
    """
    @action(detail=False, methods=['get'])
    def obtener_por_filtro(self, request):
        categoria = request.query_params.get('categoria')
        if categoria:
            queryset = Articulo.objects.filter(tipoArticulo="PDT", categoria=categoria).order_by("nombre")
        else:
            queryset = Articulo.objects.filter(tipoArticulo="PDT").order_by("nombre")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    """
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return ArticuloSerializadorInterno
        return ArticuloSerializadorExterno

class ServiciosViewset(ModelViewSet):
    queryset = Articulo.objects.filter(tipoArticulo="SRV").order_by("nombre")
    pagination_class = ArticuloPagination
    """
    @action(detail=False, methods=['get'])
    def obtener_por_filtro(self, request):
        categoria = request.query_params.get('categoria')
        if categoria:
            queryset = Articulo.objects.filter(tipoArticulo="SRV", categoria=categoria).order_by("nombre")
        else:
            queryset = Articulo.objects.filter(tipoArticulo="SRV").order_by("nombre")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    """
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return ArticuloSerializadorInterno
        return ArticuloSerializadorExterno
    
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
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return ImagenSerializerInterno
        return ImagenSerializerExterno