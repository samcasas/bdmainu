from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "www.mainu.com.mx",
    "mainu.com.mx",
    "api.mainu.com.mx",  # Incluye el subdominio para la API
]

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'mainu',  # Cambia esto por el nombre de tu base de datos
        'CLIENT': {
            'host': config('DB_HOST_MONGO'),
            'tls': True,
        }
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

CORS_ALLOWED_ORIGINS = [
    "https://www.mainu.com.mx",
    "https://mainu.com.mx",
    "https://api.mainu.com.mx",  # Agrega esto si necesitas CORS para el API
]

# Otras configuraciones opcionales
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = ['content-type']