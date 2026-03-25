# config/settings/production.py

import os
from typing import Optional

import dj_database_url

DEBUG: bool = False
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"), conn_max_age=600
    )
}

# Qo‘shimcha security settings
CSRF_COOKIE_SECURE: bool = True
SESSION_COOKIE_SECURE: bool = True
SECURE_SSL_REDIRECT: bool = True
