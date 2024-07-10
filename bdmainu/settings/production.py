from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://tu-dominio.com",
]

# Otras configuraciones opcionales
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = ['content-type']