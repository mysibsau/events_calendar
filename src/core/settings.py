from os.path import join as path_join
from pathlib import Path

import environ

env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(str(BASE_DIR) + '\\.env')
SECRET_KEY = env.str('SECRET_KEY', default='s3cr3t')

DEBUG = env.bool('DEBUG', default=False)

if DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'anymail',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'django_filters',
    'odoo_auth',

    'events',
    'user'
]

AUTHENTICATION_BACKENDS = (
    'user.backends.OdooBackend',
)

ODOO_SERVER_URL = env.str('ODOO_SERVER_URL')
ODOO_SERVER_DBNAME = env.str('ODOO_SERVER_DBNAME')
ODOO_SERVER_PORT = env.int('ODOO_SERVER_PORT', default='443')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 30,
}

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Krasnoyarsk'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = path_join(BASE_DIR, 'resources/static')

MEDIA_URL = '/media/'
MEDIA_ROOT = path_join(BASE_DIR, 'resources/media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'


EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
ANYMAIL = {
    'MAILGUN_API_KEY': env.str('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': env.str('MAILGUN_SENDER_DOMAIN')
}
DEFAULT_FROM_EMAIL = 'info@' + env.str('MAILGUN_SENDER_DOMAIN')

CELERY_BROKER_URL = env.str("CELERY_BROKER", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = env.str("CELERY_BROKER", "redis://localhost:6379/0")

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
