#serializadores para los objetos entre la base de datos y la API
from api.models import Usuario,Perfil,UsoCFDI,PasswordCuentaEspecial
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password, check_password
from api.utils import TipoCuenta
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
#serializador para autenticación
class serializadorObtenerParToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except AuthenticationFailed:
            raise AuthenticationFailed("Usuario o contraseña incorrectos")
#serializador para contraseñas de clientes a usuario
class PasswordCuentaEspecialSerializador(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 
    class Meta:
        model = PasswordCuentaEspecial
        fields = ["password", "cuentaValidada"]

    def create(self, validated_data):
        """Se asegura de que la contraseña se encripte antes de crear el objeto."""
        validated_data["password"] = make_password(validated_data["password"])  # Encripta la contraseña
        return super().create(validated_data)
    
       
#serializador para registro de usuarios
class UsoCFDISerializer(serializers.ModelSerializer):
    # Ensure 'descripcion' is optional when doing a PATCH
    descripcion = serializers.CharField(required=False)

    class Meta:
        model = UsoCFDI
        fields = ["usoCFDI", "descripcion"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.partial:  # This ensures that PATCH can accept partial updates
            for field in self.fields.values():
                field.required = False

class RegistrarPerfilSerializer(serializers.ModelSerializer):
    usoCFDI = serializers.PrimaryKeyRelatedField(
        queryset=UsoCFDI.objects.all(), required=False, allow_null=True
    )
    class Meta:
        model = Perfil
        fields = [
            "apellidos",
            "nombre",
            "telefono",
            "tipoCuenta",
            "tipoEmpleado",
            "tipoPersona",
            "RFC",
            "calle",
            "numExt",
            "numInt",
            "colonia",
            "codigoPostal",
            "localidad",
            "municipio",
            "estado",
            "nomEmpresa",
            "referencia",
            "usoCFDI",
            "cuentaBancaria",
            "CLABE",
            "Banco",
            "constanciaFiscal",
        ]
        extra_kwargs = {
            "tipoEmpleado":{"required": False, "allow_null": True},
            "tipoPersona":{"required": False, "allow_null": True},
            "RFC": {"required": False, "allow_null": True},
            "calle": {"required": False},
            "numExt": {"required": False},
            "numInt": {"required": False},
            "colonia": {"required": False},
            "codigoPostal": {"required": False},
            "localidad": {"required": False},
            "municipio": {"required": False},
            "estado": {"required": False},
            "nomEmpresa": {"required": False},
            "referencia": {"required": False},
            "usoCFDI": {"required": False, "allow_null": True},
            "cuentaBancaria": {"required": False},
            "CLABE": {"required": False},
            "Banco": {"required": False},
            "constanciaFiscal": {"required": False},
        }

    def validate(self, data):
        """Validar que los campos obligatorios estén presentes."""
        required_fields = ["apellidos","nombre", "telefono", "tipoCuenta"]
        if data["tipoCuenta"] == TipoCuenta.EMPLEADO:
            required_fields.append("tipoEmpleado")
        if data["tipoCuenta"] == TipoCuenta.PROVEEDOR or data["tipoCuenta"] == TipoCuenta.CLIENTE:
            required_fields.append("tipoPersona")
        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError({field: "Este campo es obligatorio."})
        return data

class RegistrarSerializador(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    perfil = RegistrarPerfilSerializer()

    correoElectronico = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=Usuario.objects.all(),
                message="Ya existe un/a usuario/a registrado/a con este correo electrónico."
            )
        ]
    )

    class Meta:
        model = Usuario
        fields = ["correoElectronico", "password", "perfil"]
    def create(self, validated_data):
        perfil_data = validated_data.pop("perfil")

        tipo_cuenta = perfil_data.get("tipoCuenta")
        if tipo_cuenta == TipoCuenta.EMPLEADO:
            user = Usuario.objects.create_empleado(
                correoElectronico=validated_data["correoElectronico"],
                password=validated_data["password"]
            )
        else:
            user = Usuario.objects.create_user(
                correoElectronico=validated_data["correoElectronico"],
                password=validated_data["password"]
            )

        # Aquí ya perfil_data está validado porque DRF lo validó antes de `create`
        Perfil.objects.create(usuario=user, **perfil_data)
        return user
class ValidarCuentaEspecialSerializador(serializers.ModelSerializer):
    class Meta:
        model = PasswordCuentaEspecial
        fields = ["password", "cuentaValidada"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        password = data.get("password")
        cuenta = data.get("cuentaValidada")

        # Buscar las coincidencias de cuenta
        coincidencias = PasswordCuentaEspecial.objects.filter(cuentaValidada=cuenta)
        # Verificar la contraseña
        for obj in coincidencias:
            if check_password(password, obj.password):
                data["obj_validado"] = obj  # Agregar el objeto validado a los datos
                return data

        raise serializers.ValidationError("Contraseña especial incorrecta")

class PerfilDashboardSerializador(serializers.ModelSerializer):
    usoCFDI = serializers.PrimaryKeyRelatedField(
        queryset=UsoCFDI.objects.all(), required=False, allow_null=True
    )
    correoElectronico = serializers.EmailField(source="usuario.correoElectronico", required=False)

    class Meta:
        model = Perfil
        fields = [
            "correoElectronico", "apellidos", "nombre", "telefono", "tipoCuenta",
            "tipoEmpleado", "tipoPersona", "RFC", "calle", "numExt", "numInt",
            "colonia", "codigoPostal", "localidad", "municipio", "estado",
            "nomEmpresa", "referencia", "usoCFDI", "cuentaBancaria", "CLABE",
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

        # Validar que el correo no exista en otro usuario
        if correo and correo != instance.usuario.correoElectronico:
            if Usuario.objects.filter(correoElectronico=correo).exclude(id=instance.usuario.id).exists():
                raise serializers.ValidationError({"correoElectronico": "Correo ya utilizado."})

        # Actualizar Perfil
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Actualizar Usuario
        if correo:
            usuario = instance.usuario
            usuario.correoElectronico = correo
            usuario.save()

        return instance
    
#Serializador para la app de escritorio Login   
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
class PerfilEdicionParcialSerializador(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'
        extra_kwargs = {
            field.name: {'required': False} for field in Perfil._meta.fields
        }