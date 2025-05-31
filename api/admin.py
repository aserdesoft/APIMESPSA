from django.contrib import admin
from api.models import Usuario
from api.Models.UsuarioModels import Perfil,PasswordCuentaEspecial
from api.Models.FiscalModels import UsoCFDI

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['correoElectronico']

class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario',"apellidos","nombre","telefono","tipoCuenta","tipoPersona","tipoEmpleado","RFC","calle","numExt","numInt","colonia","codigoPostal","localidad","municipio","estado",
    "nomEmpresa","referencia","usoCFDI","cuentaBancaria","CLABE","Banco","constanciaFiscal"]
    list_editable= ["apellidos","nombre","telefono","tipoCuenta","tipoPersona","tipoEmpleado","RFC","calle","numExt","numInt","colonia","codigoPostal","localidad","municipio","estado",
    "nomEmpresa","referencia","usoCFDI","cuentaBancaria","CLABE","Banco"]

class UsoCFDIAdmin(admin.ModelAdmin):
    list_display = ["usoCFDI", "descripcion"]
    search_fields = ["descripcion"]

class PasswordCuentaEspecialAdmin(admin.ModelAdmin):
    list_display = ["id"]
    search_fields = ["cuentaValidada"]



admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(UsoCFDI,UsoCFDIAdmin)
admin.site.register(PasswordCuentaEspecial,PasswordCuentaEspecialAdmin)
