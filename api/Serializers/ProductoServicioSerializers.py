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
        fields = ['id', 'archivo']

class ImagenSerializerExterno(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ['archivo']

class ArticuloSerializadorListaExterno(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), required=False, allow_null=True
    )
    imagenes = ImagenSerializerExterno(many=True, read_only=True)
    class Meta:
        model = Articulo
        fields = [
            "id","nombre", "categoria","valorUnitario", 'imagenes'
        ]

class ArticuloSerializadorIndExterno(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), required=False, allow_null=True
    )
    imagenes = ImagenSerializerExterno(many=True, read_only=True)
    class Meta:
        model = Articulo
        fields = [
            "id","nombre", "descripcion", "categoria","valorUnitario", 'imagenes'
        ]


class ArticuloSerializadorInterno(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), required=False, allow_null=True
    )
    claveUnidad = serializers.PrimaryKeyRelatedField(
        queryset=Unidad.objects.all(), required=False, allow_null=True
    )

    # Campo para recibir múltiples archivos al crear/actualizar
    archivos = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    # Campo para responder con los objetos de imagen
    imagenes = ImagenSerializerInterno(many=True, read_only=True)

    class Meta:
        model = Articulo
        fields = [
            "id", "nombre", "descripcion", "claveUnidad", "claveFiscal",
            "tipoArticulo", "categoria", "valorUnitario",
            "archivos",    # write-only
            "imagenes"     # read-only
        ]

    def create(self, validated_data):
        archivos = validated_data.pop("archivos", [])
        articulo = Articulo.objects.create(**validated_data)

        for archivo in archivos:
            Imagen.objects.create(articulo=articulo, archivo=archivo)

        return articulo

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