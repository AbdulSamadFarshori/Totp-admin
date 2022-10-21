import pyotp


def get_current_totp(value):
    totp = pyotp.TOTP(value, digits=6)
    current_totp = totp.now()
    return current_totp


def create_google_auth_uri(value):
    auth = pyotp.totp.TOTP(value).provisioning_uri(name='sumir40@google.com', issuer_name='Secure App')
    return auth