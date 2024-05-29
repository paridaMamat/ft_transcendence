from rest_framework_simplejwt.tokens import RefreshToken
from pyotp import TOTP


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def verify_otp(secret_key, otp):
    # Create a TOTP object with the secret key
    totp = TOTP(secret_key)

    # Verify the OTP
    verified = totp.verify(otp)

    return verified