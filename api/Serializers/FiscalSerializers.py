from rest_framework import serializers
from api.Models.FiscalModels import UsoCFDI
# serializador para registro de usuarios
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