# UsuarioEscritorioSerializer.py

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authentication import authenticate
from api.Models.UsuarioModels import *

# Validación simple del login
class ValidarUsuarioSimpleSerializer(serializers.Serializer):
    correoElectronico = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["correoElectronico"],
            password=data["password"]
        )
        if user is None:
            raise serializers.ValidationError("Correo o contraseña incorrectos")

        if not user.is_staff:
            raise serializers.ValidationError("No tienes permisos para acceder desde esta aplicación.")

        data["usuario"] = user
        return data

class ActualizarDatos(serializers.ModelSerializer):
    usoCFDI = serializers.PrimaryKeyRelatedField(
        queryset=UsoCFDI.objects.all(), required=False, allow_null=True
    )
    correoElectronico = serializers.EmailField(source="usuario.correoElectronico", required=False)
    RFC = serializers.CharField(
        required=False,
        validators=[
            UniqueValidator(
                queryset=Perfil.objects.all(),
                message="RFC ya utilizado"
            )
        ]
    )

    class Meta:
        model = Perfil
        fields = [
            "correoElectronico", "apellidos", "nombre", "telefono", "tipoCuenta",
            "tipoEmpleado", "tipoPersona", "RFC", "calle", "numExt", "numInt",
            "colonia", "codigoPostal", "localidad", "municipio", "estado",
            "nomEmpresa", "usoCFDI", "cuentaBancaria", "CLABE",
            "Banco", "constanciaFiscal",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('partial', True):
            for field in self.fields.values():
                field.required = False

    def validate(self, attrs):
        campos_mayus = [
            "RFC", "Banco", "cuentaBancaria", "calle", "numInt", "colonia",
            "localidad", "municipio", "estado"
        ]
        for campo in campos_mayus:
            valor = attrs.get(campo)
            if isinstance(valor, str):
                attrs[campo] = valor.upper()
        return attrs

    def update(self, instance, validated_data):
        usuario_data = validated_data.pop('usuario', {})
        correo = usuario_data.get('correoElectronico')

        if correo and correo != instance.usuario.correoElectronico:
            if Usuario.objects.filter(correoElectronico=correo).exclude(id=instance.usuario.id).exists():
                raise serializers.ValidationError({"correoElectronico": "Correo electrónico ya utilizado."})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if correo:
            usuario = instance.usuario
            usuario.correoElectronico = correo
            usuario.save()

        return instance

