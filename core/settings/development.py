# file for development
import datetime

from core.settings.base import *
from decouple import config

SECRET_KEY = config("SECRET_KEY")

# DEBUG = config('DEBUG')
DEBUG = True
ALLOWED_HOSTS = ['*']


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CORS_ORIGIN_WRITELIST= (
    'http://localhost',
)



SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
