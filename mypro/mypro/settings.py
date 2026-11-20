
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

DEBUG_SETTING = os.environ.get("DJANGO_DEBUG")
DEBUG = (
    DEBUG_SETTING.lower() in {"1", "true", "yes"}
    if DEBUG_SETTING is not None
    else not RENDER_EXTERNAL_HOSTNAME
)

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "local-development-only-key"
)

if not DEBUG and SECRET_KEY == "local-development-only-key":
    raise ValueError("Set DJANGO_SECRET_KEY in Render environment variables.")

ALLOWED_HOSTS = [
    "vtalent.in",
    "www.vtalent.in",
    "localhost",
    "127.0.0.1",
]

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

ALLOWED_HOSTS.extend(
    host.strip()
    for host in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if host.strip()
)

CSRF_TRUSTED_ORIGINS = [
    "https://vtalent.in",
    "https://www.vtalent.in",
]

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(
        f"https://{RENDER_EXTERNAL_HOSTNAME}"
    )

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "myapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mypro.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "mypro.wsgi.application"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

WHITENOISE_MANIFEST_STRICT = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

SECURE_HSTS_SECONDS = 3600 if not DEBUG else 0

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
