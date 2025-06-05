from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import (check_password,make_password,)
from django.core.exceptions import ValidationError
from api.utils import TipoPersona,TipoEmpleado,TipoCuenta
from api.Models.FiscalModels import UsoCFDI
from api.models import Usuario
class Perfil(models.Model):
    # Datos requeridos para el registro
    apellidos = models.CharField(max_length=150,default="")
    nombre = models.CharField(max_length=150,default="")
    telefono = models.CharField(max_length=10, default="")
    tipoCuenta = models.CharField(max_length=3,choices=TipoCuenta.choices,default=TipoCuenta.CLIENTE)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="perfil")
    #Datos para gestión de cuentas de proveedores y empleados
    tipoEmpleado =  models.CharField(max_length=50,choices=TipoEmpleado.choices, null=True ,default=None)
    tipoPersona = models.CharField(max_length=50,choices=TipoPersona.choices, null=True ,default=None)
    # Datos extras para completar el perfil
    RFC = models.CharField(max_length=13, unique=True, null=True, default=None)
    calle = models.CharField(max_length=300, blank=True, default="")
    numExt = models.CharField(max_length=50, blank=True, default="")
    numInt = models.CharField(max_length=50, blank=True, default="")
    colonia = models.CharField(max_length=300, blank=True, default="")
    codigoPostal = models.PositiveIntegerField(null= True,default=None)
    localidad =models.CharField(max_length=300, blank=True, default="")
    municipio = models.CharField(max_length=300, blank=True, default="")
    estado = models.CharField(max_length=50, blank=True, default="")
    nomEmpresa = models.CharField(max_length=300, blank=True, default="")
    referencia = models.CharField(max_length=300, blank=True, default="")
    #información fiscal
    usoCFDI = models.ForeignKey(UsoCFDI,to_field="usoCFDI", on_delete=models.SET_DEFAULT, null=True ,default=None,blank=True)
    cuentaBancaria = models.CharField(max_length=20, blank=True, default="")
    CLABE = models.CharField(max_length=18, blank=True, default="")
    Banco = models.CharField(max_length=100, blank=True, default="")
    constanciaFiscal = models.FileField(upload_to="constancias", blank=True, null=True)

    def clean(self):
        # Campos requeridos para cualquier usuario
        required_fields = ["apellidos","nombre", "telefono", "tipoCuenta","usuario"]
        for field in required_fields:
            value = getattr(self, field, None)
            if not value:
                raise ValidationError({field: f"Este campo es obligatorio"})
            if field == "apellidos" or field == "nombre":
                setattr(self,field,value.upper())
        

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

#Modelo para manejar las contraseñas para crear cuentas de 
class PasswordCuentaEspecial(models.Model):
    password = models.CharField(max_length=128)
    passwordVisible = models.CharField(max_length=255,unique=True)
    cuentaValidada = models.CharField(
        max_length=3,
        choices=TipoCuenta.cuentasDetrasPassword(),
        default=TipoCuenta.EMPLEADO
    )

    def save(self, *args, **kwargs):
        # Validar que no exista ninguna contraseña igual (en texto plano)
        for obj in PasswordCuentaEspecial.objects.all():
            if obj.verificar_password(self.passwordVisible):
                raise ValidationError("Esta contraseña ya está en uso.")
        # Encriptar y guardar
        self.password = make_password(self.passwordVisible)
        super().save(*args, **kwargs)

    def verificar_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.cuentaValidada} (contraseña protegida)"