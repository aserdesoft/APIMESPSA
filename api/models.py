from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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