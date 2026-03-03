# config/settings/development.py

from typing import Optional

from .base import *  # noqa: F403,F405

DEBUG: bool = True  # type: ignore[no-redef]
ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]  # type: ignore[no-redef]
CORS_ALLOW_ALL_ORIGINS: bool = True

DATABASES: dict[str, dict[str, Optional[str]]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "db.sqlite3"),  # noqa: F405
    }
}
