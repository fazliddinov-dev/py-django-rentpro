from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.user.models import EmailOTP
from apps.user.tasks import send_otp_email_task
from apps.user.utils import generate_otp
from ..utils import is_locked, register_failure, reset_attempts

User = get_user_model()


class OTPService:

    @staticmethod
    def send_otp(email: str, registration_data: dict = None) -> None:
        """
        Creates OTP and sends email asynchronously.
        Optionally stores registration_data to be used after verification.
        """
        EmailOTP.objects.filter(email=email, is_used=False).update(is_used=True)

        code = generate_otp()

        EmailOTP.objects.create(
            email=email,
            code=code,
            registration_data=registration_data,  # ← store it here
        )

        send_otp_email_task.delay(email, code)

    @staticmethod
    def verify_otp(email: str, code: str):
        """
        Verifies OTP and returns (user, created) tuple.
        - If registration_data exists on OTP → creates new user.
        - Otherwise → fetches existing user (login flow).
        """
        if is_locked(email):
            raise PermissionError("Too many failed attempts. Please try again later.")

        otp = EmailOTP.objects.filter(
            email=email,
            code=code,
            is_used=False,
        ).last()

        if not otp:
            register_failure(email)  # track failed attempt
            raise ValidationError("Invalid OTP")

        if otp.is_expired():
            raise ValidationError("OTP expired")

        # Mark OTP as used
        otp.is_used = True
        otp.used_at = timezone.now()
        otp.save(update_fields=["is_used", "used_at"])

        reset_attempts(email)  # clear failed attempts on success

        # Registration flow
        if otp.registration_data:
            user = OTPService._create_user(otp.registration_data)
            return user, True

        # Login flow — user must already exist
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("No account found. Please register first.")

        return user, False

    @staticmethod
    def _create_user(registration_data: dict) -> User:
        """Creates a new user from stored registration data."""
        from apps.user.services.register_service import register_user
        return register_user(registration_data)