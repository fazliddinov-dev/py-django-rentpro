import random

from django.core.cache import cache
from django.core.mail import send_mail


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, code):
    send_mail(
        subject="Your login code",
        message=f"Your verification code is {code}",
        from_email=None,
        recipient_list=[email],
    )


def get_client_ip(request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


MAX_OTP_ATTEMPTS = 5
LOCK_TIME_SECONDS = 600  # 10 minutes


def _fail_key(email: str) -> str:
    return f"otp_fail:{email}"


def _lock_key(email: str) -> str:
    return f"otp_lock:{email}"


def is_locked(email: str) -> bool:
    return cache.get(_lock_key(email)) is not None


def register_failure(email: str) -> int:
    key = _fail_key(email)
    attempts = cache.get(key, 0) + 1

    cache.set(key, attempts, timeout=LOCK_TIME_SECONDS)

    if attempts >= MAX_OTP_ATTEMPTS:
        cache.set(_lock_key(email), True, timeout=LOCK_TIME_SECONDS)

    return attempts


def reset_attempts(email: str):
    cache.delete(_fail_key(email))
    cache.delete(_lock_key(email))
