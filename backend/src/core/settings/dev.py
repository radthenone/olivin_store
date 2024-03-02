from src.core.settings.base import *
from dotenv import load_dotenv
# from celery.schedules import crontab

load_dotenv(PROJECT_DIR / '.envs' / 'dev' / 'django.env')
load_dotenv(PROJECT_DIR / '.envs' / 'dev' / 'postgres.env')

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = bool(os.getenv("DEBUG"))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

MIDDLEWARE += [
    'silk.middleware.SilkyMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INSTALLED_APPS += (
    'silk',
    "debug_toolbar",
    'django_extensions',
)

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': PROJECT_DIR / 'db.sqlite3',
#     }
# }


# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(BASE_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(BASE_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# # CELERY
# # ------------------------------------------------------------------------------
# if USE_TZ:
#     # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
#     CELERY_TIMEZONE = TIME_ZONE
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
# CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
# CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
# CELERY_RESULT_EXTENDED = True
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
# CELERY_ACCEPT_CONTENT = ["json"]
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
# CELERY_TASK_SERIALIZER = "json"
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
# CELERY_RESULT_SERIALIZER = "json"
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# CELERY_TASK_TIME_LIMIT = 5 * 60
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
# CELERY_TASK_SOFT_TIME_LIMIT = 60
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
# CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-schedule
# CELERY_BEAT_SCHEDULE = {
#     "clean_register_tokens": {
#         "task": "src.users.tasks",
#         "schedule": crontab(minute="*/30"),
#     }
# }

# # EMAIL
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
# DEFAULT_EMAIL = os.getenv("DEFAULT_EMAIL")
# EMAIL_HOST = os.getenv("EMAIL_HOST")
# EMAIL_PORT = os.getenv("EMAIL_PORT")
# EMAIL_HOST_USER = ""
# EMAIL_HOST_PASSWORD = ""
# EMAIL_USE_TLS = False

# DJANGO-CORS-HEADERS
# ------------------------------------------------------------------------------
# https://github.com/adamchainz/django-cors-headers#setup
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_URLS_REGEX = r"^/api/.*$"
CORS_ORIGIN_WHITELIST = (
    "http://localhost:8000",
    "https://localhost:8000",
    "http://127.0.0.1:8000",
    "https://127.0.0.1:8000",
)

# # CACHES
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/4.1/topics/cache/#redis
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": os.getenv("REDIS_URL"),
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     }
# }

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    'disable_existing_loggers': True,
    "formatters": {
        "json": {"()": "pythonjsonlogger.jsonlogger.JsonFormatter"},
    },
    "handlers": {
        'default': {
            'level': 'INFO',
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            "filename": str(BASE_DIR / "logs" / "debug.log"),
            'maxBytes': 1024 * 1024,  # 1 MB
            'backupCount': 5,
        },
    },
    "loggers": {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        "polls": {
            "handlers": ["console"],
            "level": "INFO"
        },
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
