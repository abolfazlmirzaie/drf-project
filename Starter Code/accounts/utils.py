import random
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings


OTP_LENGTH = 6
OTP_TTL_MINUTES = 10


def generate_otp_code(length=OTP_LENGTH):
    range_start = 10**(length-1)
    range_end = (10**length) -1
    return str(random.randint(range_start, range_end))

def create_and_send_otp_code(email, subject="your login code"):
    from .models import EmailOTP
    code = generate_otp_code()
    created_at = timezone.now()
    expires_at = created_at + timedelta(minutes=OTP_TTL_MINUTES)
    otp = EmailOTP(email=email, code=code, expires_at=expires_at)
    message = f"Your login code is {code}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    return otp
