from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache
import secrets

def generar_codigo(longitud=6):
    rango_min = 10**(longitud - 1)
    rango_max = (10**longitud) - 1
    return str(secrets.randbelow(rango_max - rango_min + 1) + rango_min)

@api_view(['POST'])
def send_reset_code(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email es requerido'}, status=400)

    codigo = generar_codigo(6)

    # Guardar en cache con expiración de 10 minutos (600 segundos)
    cache.set(f"reset_code_{email}", codigo, timeout=600)

    send_mail(
        'Código de restablecimiento seguro',
        f'Tu código de verificación es: {codigo}',
        'tu-correo@tudominio.com',
        [email],
        fail_silently=False,
    )

    return Response({'message': 'Correo enviado'})

@api_view(['POST'])
def verify_reset_code(request):
    email = request.data.get('email')
    codigo_enviado = request.data.get('code')

    if not email or not codigo_enviado:
        return Response({'error': 'Email y código son requeridos'}, status=400)

    codigo_cache = cache.get(f"reset_code_{email}")

    if codigo_cache is None:
        return Response({'error': 'Código expirado o no válido'}, status=400)

    if codigo_enviado == codigo_cache:
        # Código correcto: puedes borrar el código de la cache para seguridad
        cache.delete(f"reset_code_{email}")
        return Response({'message': 'Código válido'})
    else:
        return Response({'error': 'Código incorrecto'}, status=400)