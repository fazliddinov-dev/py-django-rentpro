# config/settings/production.py

import os
from typing import Optional

DEBUG: bool = False
ALLOWED_HOSTS: list[str] = os.getenv("ALLOWED_HOSTS", "").split(",")

DATABASES: dict[str, dict[str, Optional[str]]] = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# Qo‘shimcha security settings
CSRF_COOKIE_SECURE: bool = True
SESSION_COOKIE_SECURE: bool = True
SECURE_SSL_REDIRECT: bool = True
