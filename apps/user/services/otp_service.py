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
    def send_otp(email: str) -> None:
        """
        Creates OTP and sends email asynchronously.
        """

        # Invalidate previous OTPs
        EmailOTP.objects.filter(email=email, is_used=False).update(is_used=True)

        code = generate_otp()

        EmailOTP.objects.create(
            email=email,
            code=code,
        )

        # Send email async
        send_otp_email_task.delay(email, code)

    @staticmethod
    def verify_otp(email: str, code: str):
        """
        Verifies OTP and returns User.
        """

        if is_locked(email):
            raise ValidationError("Too many failed attempts. Please try again later.")

        otp = EmailOTP.objects.filter(
            email=email,
            code=code,
            is_used=False,
        ).last()

        if not otp:
            raise ValidationError("Invalid OTP")

        if otp.is_expired():
            raise ValidationError("OTP expired")

        otp.is_used = True
        otp.used_at = timezone.now()
        otp.save(update_fields=["is_used", "used_at"])

        user, _ = User.objects.get_or_create(email=email)

        return user

    @staticmethod
    def create_and_store_otp(email: str) -> str:
        """
        Creates a new OTP, marks all previous OTPs for this email as used,
        and returns the new OTP code.
        """
        # Invalidate all previous OTPs for this email
        EmailOTP.objects.filter(email=email, is_used=False).update(is_used=True)

        # Generate new OTP
        otp_code = generate_otp()

        # Store new OTP
        EmailOTP.objects.create(email=email, code=otp_code)

        return otp_code
