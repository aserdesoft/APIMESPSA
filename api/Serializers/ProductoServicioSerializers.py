from rest_framework import serializers
from api.Models.ProductoServicioModels import *
from rest_framework.validators import UniqueValidator
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
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
    imagenes = serializers.SerializerMethodField()

    class Meta:
        model = Articulo
        fields = [
            "id", "nombre", "categoria", "valorUnitario", "imagenes"
        ]

    def get_imagenes(self, obj):
        primera_imagen = obj.imagenes.first()
        if primera_imagen:
            return ImagenSerializerExterno(primera_imagen, context=self.context).data
        return []

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
    nombre = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Articulo.objects.all(),
                message="Ya existe un articulo registrado con este nombre"
            )
        ]
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
            # Abrir la imagen con Pillow
            img = Image.open(archivo)

            # Convertir a modo RGB si es necesario
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Redimensionar (por ejemplo, a 800x800 px)
            img = img.resize((275, 183))

            # Guardar en formato WebP en memoria
            buffer = BytesIO()
            img.save(buffer, format="WEBP", quality=85)  # puedes ajustar la calidad
            buffer.seek(0)

            # Crear un archivo Django desde el buffer
            nombre_archivo = archivo.name.rsplit('.', 1)[0] + ".webp"
            archivo_webp = ContentFile(buffer.read(), name=nombre_archivo)

            # Guardar la imagen procesada
            Imagen.objects.create(articulo=articulo, archivo=archivo_webp)

        return articulo

#Serializador para categorias
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["nombre","tipoArticulo"]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.partial:  # This ensures that PATCH can accept partial updates
                for field in self.fields.values():
                    field.required = False