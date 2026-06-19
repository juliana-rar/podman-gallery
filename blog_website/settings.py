# -*- coding: utf-8 -*-
from pathlib import Path
import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=['http://localhost:3000', 'http://127.0.0.1:8000'],
)

env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
environ.Env.read_env(env_file)

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)

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
    'blog',
    'events',
    'gallery',
    'herophotos',
    'projects',
    'user_profile',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',  
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
                'blog.context_processors.get_all_categories',
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