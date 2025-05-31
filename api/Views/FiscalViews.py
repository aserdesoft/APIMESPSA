from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,AllowAny
from api.Models.FiscalModels import *
from api.Serializers.FiscalSerializers import *

class UsoCFDIViewset(ModelViewSet):
    queryset = UsoCFDI.objects.all().order_by("usoCFDI")
    serializer_class = UsoCFDISerializer
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated()]