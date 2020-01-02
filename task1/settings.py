import os

import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

# Security
# -----------------------------------------------------------------------
SECRET_KEY = env.str('SECRET_KEY', "=rh-*z4ow74^8&f%z7$*l4rta3e2i&l)isuxdj0k%%4gq+#84u")
DEBUG = env.bool('DEBUG', True)
ALLOWED_HOSTS = ["*"]

# Application definition
# -----------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "task1.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "task1.wsgi.application"

# Database
# -----------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Password validation
# -----------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
# -----------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# -----------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# MEDIA
# -----------------------------------------------------------------------
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Authentication
# -----------------------------------------------------------------------
AUTH_USER_MODEL = "main_app.BaseUser"
ADMIN_USER = {
    "email": env.str('ADMIN_EMAIL_ADDRESS', "admin@admin.com"),
    "password": env.str('ADMIN_PASSWORD', "admin"),
}
LOGIN_URL = "/login/"
HOME_URL = "/home/"

# Email Verification
# -----------------------------------------------------------------------
SENDER_MAIL_CREDENTIALS = {
    "address": env.str('SENDER_EMAIL_ADDRESS', None),
    "password": env.str('SENDER_EMAIL_PASSWORD', None),
}
