from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import base64

# Load AES key from environment or fallback (32 bytes = 256-bit)
raw_key = os.environ.get("AES_SECRET_KEY")

if raw_key:
    # If using a base64-encoded key in env
    AES_KEY = base64.b64decode(raw_key)
else:
    # Fallback for dev/testing
    AES_KEY = os.urandom(32)

assert len(AES_KEY) == 32, "AES key must be 32 bytes long (256-bit)"

def generate_iv():
    return os.urandom(16)  # 128-bit IV for AES-CBC

def encrypt_data(data: bytes) -> bytes:
    iv = generate_iv()

    # Pad data to block size
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # AES encryption in CBC mode
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return iv + ciphertext  # prepend IV for use in decryption

def decrypt_data(encrypted_data: bytes) -> bytes:
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad data
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_plaintext) + unpadder.finalize()
