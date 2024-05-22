import os
import uuid
import warnings

from dotenv import load_dotenv

from src.core.config import PROJECT_DIR
from src.core.settings.base import *  # noqa

load_dotenv(PROJECT_DIR / ".envs" / "dev" / "django.env")
load_dotenv(PROJECT_DIR / ".envs" / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "test_secret_key")

DEBUG = bool(int(os.getenv("DEBUG", 1)))

ALLOWED_HOSTS = str(os.getenv("ALLOWED_HOSTS", "*")).split(",")

MIDDLEWARE += []

INSTALLED_APPS += ("django_extensions",)

DJANGO_ALLOW_ASYNC_UNSAFE = True

DJANGO_HOST = os.getenv("DJANGO_HOST", "localhost")
DJANGO_PORT = os.getenv("DJANGO_PORT", "8000")

# DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB", "postgres-olivin"),
        "USER": os.getenv("POSTGRES_USER", "olivin"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "olivin"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5433"),
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# DJANGO-CORS-HEADERS
# ------------------------------------------------------------------------------
# https://github.com/adamchainz/django-cors-headers#setup
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_URLS_REGEX = r"^/api/.*$"

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.1/topics/cache/#redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", 0)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "some_redis_password")
REDIS_EXPIRE = os.getenv("REDIS_EXPIRE", 60 * 60 * 24)
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "rich": {"datefmt": "[%X]"},
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "filters": ["require_debug_true"],
            "formatter": "rich",
            "level": "DEBUG",
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
        },
    },
    "loggers": {
        "django": {
            "handlers": [],
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}


# CELERY
# ------------------------------------------------------------------------------
if USE_TZ:
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_URL = REDIS_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = REDIS_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
CELERY_RESULT_EXTENDED = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
CELERY_TASK_TIME_LIMIT = 5 * 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
CELERY_TASK_SOFT_TIME_LIMIT = 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULE = {
    "add-every-30-seconds": {
        "task": "src.common.tasks.multiply_interval",
        "schedule": 30.0,
        "args": (10, 2),
    },
}
CELERY_SETTINGS = "django.conf:settings"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "127.0.0.1")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = os.getenv("EMAIL_PORT", 1025)
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", False)

# JWT
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 180)


# STATIC & MEDIA
# ------------------------------------------------------------------------------
# BUCKET S3 SETTINGS
USE_S3_AMAZON = bool(int(os.getenv("USE_S3_AMAZON", 0)))
BUCKET_NAME = os.getenv("BUCKET_NAME", "olivin-d2e3e393-9767-413b-b6d5-cf8fd6166de0")
STATIC_PATH = "static"
MEDIA_PATH = "media"
# AWS S3
if USE_S3_AMAZON:
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "")
    AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "")
    STATIC_URL = f"https://{BUCKET_NAME}.s3.amazonaws.com/{STATIC_PATH}/"
    MEDIA_URL = f"https://{BUCKET_NAME}.s3.amazonaws.com/{MEDIA_PATH}/"

if not USE_S3_AMAZON:
    MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "minioadmin")
    MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
    MINIO_HOST = os.getenv("MINIO_HOST", "localhost")
    MINIO_PORT = os.getenv("MINIO_PORT", "9000")
    MINIO_URL = (
        f"http://127.0.0.1:9000/"
        if MINIO_HOST == "localhost" and MINIO_PORT == "9000"
        else f"http://{MINIO_HOST}:{MINIO_PORT}/"
    )
    STATIC_URL = f"{MINIO_URL}{BUCKET_NAME}/{STATIC_PATH}/"
    MEDIA_URL = f"{MINIO_URL}{BUCKET_NAME}/{MEDIA_PATH}/"

STATICFILES_STORAGE = "src.core.storage.get_storage"
static_dir = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
STATICFILES_DIRS = [static_dir]

# WARNINGS
# ------------------------------------------------------------------------------
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")

# DELIVERS

# INPOST
