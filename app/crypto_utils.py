from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
import base64

def decrypt_seed(encrypted_seed_b64: str, private_key: RSAPrivateKey) -> str:
    encrypted_bytes = base64.b64decode(encrypted_seed_b64.strip())
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    decrypted_str = decrypted_bytes.decode('utf-8')
    if len(decrypted_str) != 64 or not all(c in '0123456789abcdef' for c in decrypted_str):
        raise ValueError("Invalid seed format")
    return decrypted_str

def sign_message(message: str, private_key: RSAPrivateKey) -> bytes:
    message_bytes = message.encode('utf-8')
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def encrypt_with_public_key(data: bytes, public_key: RSAPublicKey) -> bytes:
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def load_private_key(path: str) -> RSAPrivateKey:
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None,
        )

def load_public_key(path: str) -> RSAPublicKey:
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())
