"""
Django settings for Repositorium project.
Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from typing import Any

import jupyterlab
from django.core.exceptions import ImproperlyConfigured


def get_env(var_name: str, default: Any = None) -> str:
    if default is not None:
        return os.environ.get(var_name, default)
    try:
        return os.environ[var_name]
    except KeyError:
        raise ImproperlyConfigured(f"Set the {var_name} environment variable")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

FILE_DIR = f"{BASE_DIR}/files"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-$i2h4(x7fa9x@+vmhe%@03c(#me^_*_ke5s88wn4y@1!50yox=",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(get_env("DJANGO_DEBUG", default=False))

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "repositorium.api",
    "repositorium.users",
    "repositorium.learning_resources",
    "repositorium.recomendations",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "repositorium.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "repositorium.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_env("POSTGRES_DB", "postgres"),
        "USER": get_env("POSTGRES_USER", "postgres"),
        "PASSWORD": get_env("POSTGRES_PASSWORD", "postgres"),
        "HOST": get_env("POSTGRES_HOST", "db"),
        "PORT": get_env("POSTGRES_PORT", 5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DJANGO_ALLOW_ASYNC_UNSAFE = True

## Jupyter stuff
SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True
NOTEBOOK_ARGUMENTS = [
    "--ip",
    "0.0.0.0",
    "--port",
    "8001",
    "--allow-root",
    "--no-browser",
    "--NotebookApp.default_url",
    "/lab",
]

IPYTHON_ARGUMENTS = [
    "--ext",
    "django_extension.managements.notebook_extension",
    "--debug",
]

IPYTHON_KERNEL_DISPLAY_NAME = "Django Shell-Plus"

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "content-disposition",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
