import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

BASE_DIR = Path(__file__).resolve().parent.parent
from django.contrib import messages

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECRET_KEY = os.environ["SECRET_KEY"]
SECRET_KEY = 'asdfghjkl'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.environ.get("DEBUG", False)
DEBUG = False

# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
ALLOWED_HOSTS = ["*"]

SITE_URL = "https://live-production-frontend.herokuapp.com"
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "corsheaders",
    "rest_framework",
    "channels",
    "drf_yasg",
    "django_rest_passwordreset",
    "knox",
    "ckeditor",
    # "authentication", Deprecated
    # "main", Deprecated
    # "payments",
    "blogs",
    "danube",
    "danube.accounts",
    "danube.landing",
    "danube.profiles",
    "danube.quotes",
    "danube.contracts",
    "danube.chat",
    "danube.payments",
    "djstripe",

]

AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django_currentuser.middleware.ThreadLocalUserMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "danube.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "danube.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        # "ENGINE": "django.db.backends.postgresql",
        # "NAME": os.environ.get("DB_NAME"),
        # "USER": os.environ.get("DB_USER"),
        # "PASSWORD": os.environ.get("DB_PASSWORD"),
        # "HOST": os.environ.get("DB_HOST"),
        
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'danube',
        # 'USER': 'danube',
        # 'PASSWORD': 'postgres',
        # 'HOST': '127.0.0.1',
        # 'PORT': '5432',

        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'dbrfuiafp9vn8c',
        # 'USER': 'cfgetzqfccsfbg',
        # 'PASSWORD': 'e3ecd0e5876d100a3e38192e8fd358d4d8dedc87e1c650fd92d9c7fd6829e040',
        # 'HOST': 'ec2-3-209-39-2.compute-1.amazonaws.com',
        # 'PORT': '5432',

        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dccbv1gqjpulsf',
        'USER': 'ktnqiccdifwsdw',
        'PASSWORD': 'a77fd21dd6c08ead03b8b3339bd5f333ba5d62a2329a35945c843715c146d119',
        'HOST': 'ec2-34-247-172-149.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.QueryParameterVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1"],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "PAGE_SIZE": 10,
}
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Etc/GMT-1"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "danube/static")]
MEDIAFILES_DIRS = [os.path.join(BASE_DIR, "danube/media")]
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MESSAGE_TAGS = {messages.ERROR: "danger"}

LOGIN_URL = "/login"

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"

# email smtp settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.zoho.eu"
EMAIL_HOST_USER = "support@billntrade.com"
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST_PASSWORD = "kDJ6WMhZdCni"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# --


# STRIPE_TEST_PUBLIC_KEY = 'pk_test_HBCFcgwjSOhZlTyt3hGbIYu000R47fJFJP'
# STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY")

STRIPE_PUBLISHABLE_KEY = 'pk_live_51FYbtmJ6vXfsezRx5F7Az4fOk628W8MUPcHUce2whvQwedbBYYa3RwYrjNfPF1ODdfg0HThgP29FGfGk5BHaEQJF00NOeveJlq'
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

DJSTRIPE_WEBHOOK_SECRET = 'whsec_1bgp8fuJz7kxzHNRgfiuLrobb68RWxO8'

STRIPE_LIVE_MODE = True  # Change to True in production
DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"  # Set to `"id"` for all new 2.4+ installations

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# CSRF_TRUSTED_ORIGINS = ["*"]  # Change to url in production
# CSRF_COOKIE_NAME = "csrfToken"

# CORS_ALLOW_CREDENTIALS = not DEBUG
CORS_ALLOW_HEADERS = "*"
CORS_ORIGIN_ALLOW_ALL = True

# change to https://app.example.com in production settings
# if "*" in ALLOWED_HOSTS:
#     CORS_ALLOWED_ORIGINS = ["http://*"]
# else:
#     CORS_ALLOWED_ORIGINS = ALLOWED_HOSTS


SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

SENTRY_DSN = os.environ.get("SENTRY_DSN", None)
ENV = os.environ.get("SENTRY_DSN", "dev")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        environment=ENV,
    )

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=30),
}

# FRONTEND_URL = os.environ.get("FRONTEND_URL")

FRONTEND_URL="https://live-production-frontend.herokuapp.com"

ASGI_APPLICATION = "danube.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [str(os.environ.get("REDIS_URL"))],
        },
    },
}
