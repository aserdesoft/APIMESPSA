from rest_framework import serializers
from api.Models.ProductoServicioModels import *
#serializador para registro de Unidades
class UnidadSerializer(serializers.ModelSerializer):
    descripcion = serializers.CharField(required=False)

    class Meta:
        model = Unidad
        fields = ["claveUnidad", "descripcion"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.partial:
            for field in self.fields.values():
                field.required = False

class ImagenSerializerInterno(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ['id', 'archivo', 'articulo']

class ImagenSerializerExterno(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ['archivo']

class ArticuloSerializadorExterno(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), required=False, allow_null=True
    )
    imagenes = ImagenSerializerExterno(many=True, read_only=True)
    class Meta:
        model = Articulo
        fields = [
            "id","nombre", "descripcion", "tipoArticulo", "categoria","valorUnitario", 'imagenes'
        ]
class ArticuloSerializadorInterno(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), required=False, allow_null=True
    )
    claveUnidad = serializers.PrimaryKeyRelatedField(
        queryset=Unidad.objects.all(), required=False, allow_null=True
    )
    imagenes = ImagenSerializerInterno(many=True, read_only=True)
    class Meta:
        model = Articulo
        fields = [
            "id","nombre", "descripcion","claveUnidad","claveFiscal", "tipoArticulo", "categoria","valorUnitario", 'imagenes'
        ]

#Serializador para categorias
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["nombre"]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.partial:  # This ensures that PATCH can accept partial updates
                for field in self.fields.values():
                    field.required = False