import qrcode
import io

class QRcodeManager():

    @staticmethod
    def generate_qrcode(uri):
        """Generate qr code for adding TOTP key to an authenticator"""
        
        qr = qrcode.make(uri)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        binary_data = buf.getvalue()

        return binary_data

