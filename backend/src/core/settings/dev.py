import os

from dotenv import load_dotenv

from src.core.config import PROJECT_DIR
from src.core.settings.base import *  # noqa

load_dotenv(PROJECT_DIR / ".envs" / "dev" / "django.env")

SECRET_KEY = os.getenv("SECRET_KEY", "test_secret_key")

DEBUG = bool(os.getenv("DEBUG", 1))

ALLOWED_HOSTS = str(os.getenv("ALLOWED_HOSTS", "*")).split(",")

MIDDLEWARE += []

INSTALLED_APPS += ("django_extensions",)

DJANGO_ALLOW_ASYNC_UNSAFE = True

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

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = BASE_DIR / "staticfiles"
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [BASE_DIR / "static"]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = BASE_DIR / "media"
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

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
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "some_redis_password")
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD,
        },
    }
}


# LOGGING
# ------------------------------------------------------------------------------
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": True,
#     "formatters": {
#         "json": {"()": "pythonjsonlogger.jsonlogger.JsonFormatter"},
#     },
#     "handlers": {
#         "default": {
#             "level": "INFO",
#             "class": "logging.StreamHandler",
#             "formatter": "json",
#         },
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "json",
#         },
#         "file": {
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": str(BASE_DIR / "logs" / "debug.log"),
#             "maxBytes": 1024 * 1024,  # 1 MB
#             "backupCount": 5,
#         },
#     },
#     "loggers": {
#         "": {"handlers": ["default"], "level": "INFO", "propagate": True},
#         "polls": {"handlers": ["console"], "level": "INFO"},
#         "django": {
#             "handlers": ["file"],
#             "level": "DEBUG",
#             "propagate": True,
#         },
#     },
# }

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
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-schedule
CELERY_BEAT_SCHEDULE = {
    # "clean_register_tokens": {
    #     "task": "apps.users.tasks.clean_expired_register_tokens",
    #     "schedule": crontab(minute="*/30"),
    # }
}

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

# STORAGES

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
