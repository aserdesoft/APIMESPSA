from django.db import models
#Modelo para manejar información de CFDI
class UsoCFDI(models.Model):
    usoCFDI = models.CharField(max_length = 3, unique=True,primary_key=True)
    descripcion = models.CharField(max_length=100,default="", blank=True)
    def __str__(self):
        return self.descripcion