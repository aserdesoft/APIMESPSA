from rest_framework import serializers
from rest_framework.authentication import authenticate
#Serializadores de la app de escritorio
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