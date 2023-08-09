import base64
from google_auth_pb2 import MigrationPayload
import pyotp

def decode_protobuf(payload):
    migration_payload = MigrationPayload()
    migration_payload.ParseFromString(payload)
    return migration_payload

def convert_secret_to_base32(secret_binary):
    """Convert sec to base32."""
    return base64.b32encode(secret_binary).decode("utf-8")

def decode(data):
    buffer = base64.b64decode(data)
    payload = decode_protobuf(buffer)
    return payload

def main():
    data = "YOUR_OTP_BASE64_URI_HERE"
    
    decoded_payload = decode(data)
    #print(decoded_payload)

    # recup le premier secret, pas besoin des autres
    if decoded_payload.otp_parameters:
        secret_binary = decoded_payload.otp_parameters[0].secret
        secret_base32 = convert_secret_to_base32(secret_binary)

    secret = secret_base32

    # Création d'une instance TOTP avec la clé secrète
    totp = pyotp.TOTP(secret)

    # Générer un OTP
    print(totp.now())

main()
