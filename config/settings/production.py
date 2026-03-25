# config/settings/production.py

import os
from typing import Optional

import dj_database_url

from .base import *

DEBUG: bool = False
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS: bool = True


DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}
