from django.db import models

class TipoCuenta(models.TextChoices):
    CLIENTE = "CLI", "Cliente"
    PROVEEDOR = "PRO", "Proveedor"
    EMPLEADO = "EMP", "Empleado"

    @classmethod
    def cuentasDetrasPassword(cls):
        # Filtra las opciones deseadas a partir de cls.choices
        return [
            choice for choice in cls.choices
            if choice[0] in [cls.PROVEEDOR, cls.EMPLEADO]
        ]
    @classmethod
    def combinaciones(cls):
        combinaciones = []
        # Cliente: combinar con TipoPersona
        for persona in TipoPersona.choices:
            codigo = f"{cls.CLIENTE}-{persona[0]}"
            label = f"{cls.CLIENTE.label}-{persona[1]}"
            combinaciones.append((codigo, label))

        # Proveedor: combinar con TipoPersona
        for persona in TipoPersona.choices:
            codigo = f"{cls.PROVEEDOR}-{persona[0]}"
            label = f"{cls.PROVEEDOR.label}-{persona[1]}"
            combinaciones.append((codigo, label))

        # Empleado: combinar con TipoEmpleado
        for tipo_emp in TipoEmpleado.choices:
            codigo = f"{cls.EMPLEADO}-{tipo_emp[0]}"
            label = f"{cls.EMPLEADO.label}-{tipo_emp[1]}"
            combinaciones.append((codigo, label))

        return combinaciones
    @classmethod
    def personas(cls):
        personas = []
        for persona in TipoPersona.choices:
            codigo = f"{persona[0]}"
            label = f"{persona[1]}"
            personas.append((codigo, label))
        return personas

class TipoPersona(models.TextChoices):
    PERSONA_FISICA = "PF","Persona Física"
    PERSONA_MORAL = "PM","Persona Moral"

class TipoEmpleado(models.TextChoices):
    ADMINISTRATIVO ="ADMIN","Administrativo"
    SERVICIOS = "SERV","Servicios"
    FINANZAS = "FIN","Finanzas"

