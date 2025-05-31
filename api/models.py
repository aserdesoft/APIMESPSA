from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import (check_password,make_password,)
from api.utils import *

#Modelo para manejar información de CFDI
class UsoCFDI(models.Model):
    usoCFDI = models.CharField(max_length = 3, unique=True,primary_key=True)
    descripcion = models.CharField(max_length=100,default="", blank=True)
    def __str__(self):
        return self.descripcion
#Modelo para manejar las contraseñas para crear cuentas de 
class PasswordCuentaEspecial(models.Model):
    password = models.CharField(max_length=128)
    passwordVisible = models.CharField(max_length=300,unique=True)
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
#Modelos para el manejo de usuarios
class UsuarioManager(BaseUserManager):
    #metodo encargado de crear usuarios
    def create_user(self, correoElectronico, password=None):
        if not correoElectronico:
            raise ValueError("El usuario debe tener un correo electrónico")
        user = self.model(correoElectronico=self.normalize_email(correoElectronico))
        user.set_password(password)
        user.save(using=self._db)
        return user
    #metodo encargado de crear superusuarios
    def create_superuser(self, correoElectronico, password):
        user = self.create_user(correoElectronico, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    def create_empleado(self,correoElectronico,password):
        user = self.create_user(correoElectronico, password)
        user.is_staff = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    correoElectronico = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UsuarioManager()

    USERNAME_FIELD = "correoElectronico"

    def __str__(self):
        return self.get_username()

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

#Modelos para el manejo de productos/servicios
class Unidad(models.Model):
    claveUnidad = models.CharField(max_length = 10, unique=True,primary_key=True)
    descripcion = models.CharField(max_length=100,default="", blank=True)
    def __str__(self):
        return self.descripcion

class Categoria(models.Model):
    nombre = models.CharField(max_length=500,primary_key=True)

class Articulo(models.Model):
    nombre = models.CharField(max_length=300,default="")
    descripcion = models.TextField(default="")
    claveUnidad = models.ForeignKey(Unidad,to_field="claveUnidad", on_delete=models.SET_DEFAULT, null=True ,default=None,blank=True)
    claveFiscal = models.CharField(max_length=8, blank=True, default="")
    tipoArticulo = models.CharField(max_length=3,choices=TipoArticulo,default=TipoArticulo.PRODUCTO)
    categoria = models.ForeignKey(Categoria,to_field="nombre", on_delete=models.SET_DEFAULT, null=True ,default=None,blank=True)
    valorUnitario = models.DecimalField(decimal_places=2,max_digits=12,null=True,default=None)

class Imagen(models.Model):
    archivo = models.FileField(upload_to="imagenes",blank=True, null=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE,related_name="imagenes")
