from django.db import models
from api.utils import TipoArticulo
#Modelos para el manejo de productos/servicios
class Unidad(models.Model):
    claveUnidad = models.CharField(max_length = 10, unique=True,primary_key=True)
    descripcion = models.CharField(max_length=100,default="", blank=True)
    def __str__(self):
        return self.descripcion

class Categoria(models.Model):
    nombre = models.CharField(max_length=500,primary_key=True)
    tipoArticulo = models.CharField(max_length=3,choices=TipoArticulo,default=TipoArticulo.PRODUCTO)

class Articulo(models.Model):
    nombre = models.CharField(max_length=300,default="",unique=True)
    descripcion = models.TextField(default="")
    claveUnidad = models.ForeignKey(Unidad,to_field="claveUnidad", on_delete=models.SET_DEFAULT, null=True ,default=None,blank=True)
    claveFiscal = models.CharField(max_length=8, blank=True, default="")
    tipoArticulo = models.CharField(max_length=3,choices=TipoArticulo,default=TipoArticulo.PRODUCTO)
    categoria = models.ForeignKey(Categoria,to_field="nombre", on_delete=models.SET_NULL, null=True ,default=None,blank=True)
    valorUnitario = models.DecimalField(decimal_places=2,max_digits=12,null=True,default=None)

class Imagen(models.Model):
    archivo = models.ImageField(upload_to="imagenes",blank=True, null=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE,related_name="imagenes")