#serializadores para los objetos entre la base de datos y la API
from api.models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password, check_password
from api.utils import TipoCuenta
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator

