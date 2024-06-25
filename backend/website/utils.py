from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.base import ContentFile
from urllib.parse import urlparse
from pyotp import TOTP
import requests
import os
import uuid

##################################################
#                                                #
#      functions for 2factors Authentification   #
#                                                #
##################################################

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

##################################################
#                                                #
#      function to retrieve avatars' file        #
#                                                #
##################################################

def get_file_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join('avatars/', filename)


def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return ContentFile(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None

def get_image_filename(url, username):
    parsed_url = urlparse(url)
    file_name, file_extension = os.path.splitext(os.path.basename(parsed_url.path))
    return f"{username}_avatar{file_extension}"
