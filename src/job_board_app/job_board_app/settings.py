"""
Django settings for job_board_app project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from job_board_app.logger_formatter import ContextFormatter

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Set environment variables from .env file
load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = os.environ["DEBUG_MODE"]


ALLOWED_HOSTS: list = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    "rest_framework",
    "rest_framework.authtoken",
    # internal
    'core',
    # 3-rd party
    "drf_yasg",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.presentation.web.middleware.BlockURLMiddleware',
    'core.presentation.web.middleware.TransferRandomMessageMiddleware',
]

ROOT_URLCONF = 'job_board_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core', 'presentation', 'web', 'templates')],
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

FORM_RENDERER = "job_board_app.template_renders.CustomFormRenderer"

WSGI_APPLICATION = 'job_board_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
        'ATOMIC_REQUESTS': True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR.parents[2], "media_files", "job_board_app")

MEDIA_URL = "media/"


# Logging settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_format': {
            '()': ContextFormatter,
            'format': "[{asctime}] - {levelname} - {name} - {module}:{funcName}:{lineno} - {message}",
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': "{",
        },
    },
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'main_format',
            'level': os.environ['LOG_LEVEL'],
        },
        'file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'main_format',
            'filename': 'inform.log',
            'level': os.environ["LOG_LEVEL"],
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console_handler', 'file_handler'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'propagate': False,
        },
        'django': {
            'level': os.environ["LOG_LEVEL"],
            'handlers': ['console_handler', 'file_handler'],
            'propagate': False,
        },
        "PIL": {
            "level": 'WARNING',
            'handlers': ['console_handler', 'file_handler'],
        },
    },
}

LOG_LEVEL = os.environ["LOG_LEVEL"]

# Confirmation code settings (needed for user confirmation by email)

CONFIRMATION_CODE_LIVETIME = 3600

# SMTP server settings

EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_BACKEND = os.environ['EMAIL_BACKEND']
EMAIL_FROM = os.environ['EMAIL_FROM']

SERVER_HOST = os.environ['SERVER_HOST']


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ["REDIS_URL"],
    }
}

# REST_FRAMEWORK settings

LOGIN_URL = '/signin/'
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_RATES": {"user": "1000/day"},
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}

SWAGGER_SETTINGS = {
    "LOGOUT_URL": "/logout/",
    "LOGIN_URL": "/signin/",
}
