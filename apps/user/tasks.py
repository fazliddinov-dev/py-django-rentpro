from celery import shared_task

from apps.user.utils import send_otp_email


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def send_otp_email_task(self, email, code):
    """
    Sends OTP email to the given email.
    """
    send_otp_email(email, code)
