# -*- coding: utf-8 -*-
from pathlib import Path
import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)
# Cargar variables desde .env (en desarrollo). En producción, compose las
# inyecta vía env_file; read_env NO sobreescribe las ya presentes en el entorno.
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=['http://localhost:3000', 'http://127.0.0.1:8000'],
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
    }
}
STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'assets')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Almacenamiento de estáticos: WhiteNoise comprime los archivos al ejecutar
# collectstatic. Usamos la variante sin "manifest" (no renombra con hash) para
# evitar errores si alguna plantilla referencia un estático inexistente.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'assets')
SASS_PROCESSOR_ENABLED = False
SASS_PROCESSOR_AUTO_INCLUDE = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user_profile.User'

CKEDITOR_UPLOAD_PATH = "uploads/"
# El editor se ajusta siempre al ancho de su contenedor (el div del formulario),
# así nunca se desborda por la derecha.
CKEDITOR_CONFIGS = {
    'default': {
        'width': '100%',
    },
}
CRISPY_TEMPLATE_PACK = 'bootstrap4'

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=['127.0.0.1', 'localhost'])

   
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'miscellany',
    'products',
    'gallery',
    'herophotos',
    'user_profile',
    'ckeditor',
    'ckeditor_uploader',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise sirve los estáticos directamente desde la app (útil si no hay
    # nginx delante, p. ej. en un PaaS). Debe ir justo tras SecurityMiddleware.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', 
  
]
ROOT_URLCONF = 'blog_website.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'gallery.context_processors.gallery_context',
                'herophotos.context_processors.hero_photos',
                'user_profile.context_processors.site_settings',
            ],
        },
    },
]
WSGI_APPLICATION = 'blog_website.wsgi.application'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
AUTHENTICATION_BACKENDS = (
    "user_profile.backends.EmailAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend"
)

# ---------------------------------------------------------------------------
# Producción: la app corre detrás de nginx (reverse proxy). nginx reenvía el
# esquema original en la cabecera X-Forwarded-Proto.
# ---------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Endurecimiento que solo aplica con DEBUG=False (producción).
if not DEBUG:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_HTTPONLY = True
    X_FRAME_OPTIONS = "DENY"

    # Activá estos en .env.prod CUANDO tengas TLS (HTTPS) delante. Si los dejás
    # en True sin certificado, el sitio entra en bucle de redirección.
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
    SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)
    CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=False)
    SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)
    if SECURE_HSTS_SECONDS:
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True

# Logs a la consola (los recoge `podman logs`).
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[{asctime}] {levelname} {name}: {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": env("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
    },
}