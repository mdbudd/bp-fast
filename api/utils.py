def create_access_token(payload):
    import jwt
    from cryptography.hazmat.primitives import serialization

    with open("certs/private.ec.key", "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    key = private_key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
    )
    return jwt.encode(payload, key, algorithm="ES256")


def decode_token(token: str) -> dict:
    import jwt

    with open("certs/public.pem", "rb") as key_file:
        public_key = key_file.read()

    return jwt.decode(token, public_key, algorithms=["ES256"])


def verify_jwt(token: str) -> bool:
    isTokenValid: bool = False
    try:
        payload = decode_token(token)
    except:
        payload = None
    if payload:
        isTokenValid = True
    return isTokenValid
