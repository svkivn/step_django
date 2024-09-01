"""
Django settings for itstep project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-$_62*=c!j1xy4&&+mfznqnn@l48@muzat3f+@mr1$p36j1*twt"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = ["crispy_forms", "crispy_bootstrap4", "debug_toolbar", "django.contrib.admin", "django.contrib.auth",
    "django.contrib.contenttypes", "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "portfolio", 'blog.apps.BlogConfig', 'django_extensions', 'accounts', ]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware", "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware", ]

ROOT_URLCONF = "itstep.urls"

TEMPLATES = [
    {"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [os.path.join(BASE_DIR, "itstep/templates")],
        # Додаткові директорії
        "APP_DIRS": True,  # Вказує Django автоматично шукати шаблони в папках app
        "OPTIONS": {"context_processors": ["django.template.context_processors.debug",
            "django.template.context_processors.request", "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages", ], }, }, ]

# https://stackoverflow.com/questions/75495403/django-returns-templatedoesnotexist-when-using-crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

WSGI_APPLICATION = "itstep.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3", }}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator", },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", }, ]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# визначає URL, за яким будуть доступні статичні файли. Важливо, що це не фізичний шлях на сервері, а URL-адреса,
# за якою клієнти (браузери) будуть звертатися до статичних файлів
STATIC_URL = "/static/"

# Додаткові директорії до статичних директорій app, в яких Django буде шукати статичні файли.
# Наприклад, якщо є app blog, і у нього є директорія blog/static/, то статичні файли з цієї директорії будуть доступні.
# Можуть використовувати кілька додатків.
# При розробці Django обслуговує файли безпосередньо з директорій, вказаних у STATICFILES_DIRS.
# Порядок завантаження файлів визначається пошуком у додатках і директоріях, вказаних у STATICFILES_DIRS по порядку визначення.
STATICFILES_DIRS = [BASE_DIR / "static"]

# Директорія, куди будуть збиратися статичні файли після виконання collectstatic (використовується на продакшні)
# Всі статичні файли збираються в одному місці для ефективного обслуговування
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# URL для доступу до медіафайлів
MEDIA_URL = '/media/'

# Директорія на сервері, де будуть зберігатися медіафайли
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = ["127.0.0.1", ]

LOGGING = {'version': 1, 'filters': {'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue', }},
    'handlers': {'console': {'level': 'DEBUG', 'filters': ['require_debug_true'], 'class': 'logging.StreamHandler', }},
    'loggers': {'django.db.backends': {'level': 'DEBUG', 'handlers': ['console'], }}}

import environ

# Ініціалізація django-environ
env = environ.Env()
# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
