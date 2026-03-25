# config/settings/production.py

import os
from typing import Optional

import dj_database_url

DEBUG: bool = False
ALLOWED_HOSTS = ["*"]

DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}
