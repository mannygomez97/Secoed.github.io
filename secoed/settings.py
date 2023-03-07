import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd!m50t)w$$&ff(*pn7%oqw-1yxo+eub*xcxd^8pzo=*2)ynq=w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['95.216.216.98', '127.0.0.1', 'localhost', '194.163.151.250', '5.161.135.79']

# Base APP

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'django_celery_beat',
    'django_celery_results',
    
]

# Third Party App

THIRD_APPS = [
    'crispy_forms',
    'widget_tweaks',
    'import_export',
    'corsheaders',
    'django_filters',
    'bootstrapform',
]

# Local App

LOCAL_APPS = [
    'layout',
    'authentication',
    'conf',
    'cursos',
    'eva',
    'asesor',
    'components',
    'easyaudit',
    'docentes',
    'notify',
    'repositorio',
    'analisis'
    
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS

AUTH_USER_MODEL = 'authentication.Usuario'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'secoed.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'secoed.initialize.load_menu',
                'secoed.custom_context_processors.notifications'
            ],
        },
    },
]

WSGI_APPLICATION = 'secoed.wsgi.application'
ASGI_APPLICATION = 'secoed.asgi.application'


# CONEXION PRODUCCION
""" CONEXION_NAME = 'db_secoedv2'
CONEXION_USER = 'secoed'
CONEXION_PASSWORD = 'secoed2021'
CONEXION_HOST = 'pgdb'
CONEXION_PORT = 5432 """

# CONEXION DEVELOPER
CONEXION_NAME = 'db_secoed_v3'
CONEXION_USER = 'postgres'
CONEXION_PASSWORD = '123456'
CONEXION_HOST = 'localhost'
CONEXION_PORT = 5432

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': CONEXION_NAME,
        'USER': CONEXION_USER,
        'PASSWORD': CONEXION_PASSWORD,
        'HOST': CONEXION_HOST,
        'PORT': CONEXION_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# SMTP Configure
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'secoed.web@gmail.com'
EMAIL_HOST_PASSWORD = 'ovlmxrmaqfayaewb'
DEFAULT_FROM_EMAIL = 'secoed.web@gmail.com'

LOGIN_REDIRECT_URL = '/authentication/pages-login'
LOGOUT_REDIRECT_URL = '/authentication/pages-login'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = True

DJANGO_EASY_AUDIT_ADMIN_SHOW_MODEL_EVENTS = False
DJANGO_EASY_AUDIT_ADMIN_SHOW_AUTH_EVENTS = False
DJANGO_EASY_AUDIT_ADMIN_SHOW_REQUEST_EVENTS = False

TOKEN_MOODLE = 'f3daa936736c02613b285fe50f4616a5'
TOKEN_ROOT = '2fb3df9ba2006ef257f072651b547b3d'
API_BASE = 'https://secoed.com/aula-virtual/webservice/rest/server.php'
CONTEXT_ID = 116

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

SERVER_HOST = 'http://5.161.135.79:8086/'

# CELERY SETTINGS
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SELERLIZER = 'json'
CELERY_TIMEZONE = 'America/Guayaquil'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
