import pyotp

class TOTPManager():
    """TOTPManager - class that handle all operation, that related to TOTP"""

    @staticmethod
    def generate_totp():
        """Generate a totp for every user and add it to database"""

        key = pyotp.random_base32()
        return key

    @staticmethod
    def verify_totp(secret_key, user_code):
        """Get user secret key and code that user has sent in the login template to get access to the main page"""

        totp = pyotp.TOTP(secret_key)
        return totp.verify(user_code)
    


