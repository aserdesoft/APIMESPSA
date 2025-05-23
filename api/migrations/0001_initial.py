# Generated by Django 5.1.5 on 2025-04-09 02:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordCuentaEspecial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('cuentaValidada', models.CharField(choices=[('PRO', 'Proveedor'), ('EMP', 'Empleado')], default='EMP', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UsoCFDI',
            fields=[
                ('usoCFDI', models.CharField(max_length=3, primary_key=True, serialize=False, unique=True)),
                ('descripcion', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('correoElectronico', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apellidos', models.CharField(default='', max_length=150)),
                ('nombre', models.CharField(default='', max_length=150)),
                ('telefono', models.CharField(default='', max_length=20)),
                ('tipoCuenta', models.CharField(choices=[('CLI', 'Cliente'), ('PRO', 'Proveedor'), ('EMP', 'Empleado')], default='CLI', max_length=50)),
                ('tipoEmpleado', models.CharField(choices=[('ADMIN', 'Administrativo'), ('SERV', 'Servicios'), ('FIN', 'Finanzas')], default=None, max_length=50, null=True)),
                ('tipoPersona', models.CharField(choices=[('PF', 'Persona Física'), ('PM', 'Persona Moral')], default=None, max_length=50, null=True)),
                ('RFC', models.CharField(default=None, max_length=13, null=True, unique=True)),
                ('calle', models.CharField(blank=True, default='', max_length=300)),
                ('numExt', models.PositiveIntegerField(default=None, null=True)),
                ('numInt', models.PositiveIntegerField(default=None, null=True)),
                ('colonia', models.CharField(blank=True, default='', max_length=300)),
                ('codigoPostal', models.PositiveSmallIntegerField(default=None, null=True)),
                ('localidad', models.CharField(blank=True, default='', max_length=300)),
                ('municipio', models.CharField(blank=True, default='', max_length=300)),
                ('estado', models.CharField(blank=True, default='', max_length=50)),
                ('nomEmpresa', models.CharField(blank=True, default='', max_length=300)),
                ('referencia', models.CharField(blank=True, default='', max_length=300)),
                ('cuentaBancaria', models.CharField(blank=True, default='', max_length=20)),
                ('CLABE', models.CharField(blank=True, default='', max_length=18)),
                ('Banco', models.CharField(blank=True, default='', max_length=100)),
                ('constanciaFiscal', models.BinaryField(null=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
                ('usoCFDI', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='api.usocfdi')),
            ],
        ),
    ]
