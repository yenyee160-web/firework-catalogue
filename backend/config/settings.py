"""Minimal stateless Django configuration: no ORM, migrations, users or database."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIST = BASE_DIR / "web-dist"
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "development-only-not-for-deployment"
    else:
        raise RuntimeError("Set DJANGO_SECRET_KEY in production")
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]
INSTALLED_APPS = ["django.contrib.staticfiles"]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
DATABASES = {}
TEMPLATES = []
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kuala_Lumpur"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# WhiteNoise publishes Vite's built /assets directory without a separate web server.
WHITENOISE_ROOT = WEB_DIST
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
