from datetime import timedelta

from decouple import config

SECRET_KEY = config("SECRET_KEY")

# DEBUG = config("DEBUG", default=False, cast=bool)
DEBUG = False
ALLOWED_HOSTS = ['*']

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    }
}

CORS_ORIGIN_WRITELIST= (
    'http://localhost',
)

CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:88" "http://web:8080",
    "http://web:80",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
]
