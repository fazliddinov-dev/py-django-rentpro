# config/settings/development.py

from typing import Optional

from .base import BASE_DIR  # aniq import

DEBUG: bool = True
ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]
CORS_ALLOW_ALL_ORIGINS: bool = True

DATABASES: dict[str, dict[str, Optional[str]]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "db.sqlite3"),  # <-- Path -> str
    }
}
