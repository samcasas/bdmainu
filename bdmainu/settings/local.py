from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost"  # Incluye el subdominio para la API
]

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'mainu',
        'CLIENT': {
             'host':'localhost',
             'port':27017
            }
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",  # Agrega esto si necesitas CORS para el API
]

