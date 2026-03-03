# config/settings/__init__.py
# ENV ga qarab switch qilinadi
import os

from .development import ALLOWED_HOSTS as DEV_ALLOWED_HOSTS
from .development import DATABASES as DEV_DATABASES
from .development import DEBUG as DEV_DEBUG
from .production import ALLOWED_HOSTS as PROD_ALLOWED_HOSTS
from .production import DATABASES as PROD_DATABASES
from .production import DEBUG as PROD_DEBUG

ENV = os.getenv("ENV", "dev")

if ENV == "dev":
    DEBUG = DEV_DEBUG
    DATABASES = DEV_DATABASES
    ALLOWED_HOSTS = DEV_ALLOWED_HOSTS
elif ENV == "prod":
    DEBUG = PROD_DEBUG
    DATABASES = PROD_DATABASES
    ALLOWED_HOSTS = PROD_ALLOWED_HOSTS
else:
    raise ValueError(f"Unknown ENV: {ENV}")
