from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
import base64
import os

def encryptPassword(password):
    secret_key = os.environ.get('SECRET_KEY')
    
    # Generar un hash SHA-512 de la clave secreta
    hashed_key = hashlib.sha512(secret_key.encode()).digest()
    aes_key = hashed_key[:16]
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(b'\0' * 16), backend=default_backend())
    encryptor = cipher.encryptor()

    # Rellenar la contraseña para que tenga una longitud múltiplo de 16
    password_padded = password.ljust((len(password) // 16 + 1) * 16)
    encrypted_password = encryptor.update(password_padded.encode()) + encryptor.finalize()
    encrypted_password_base64 = base64.b64encode(encrypted_password).decode()

    return encrypted_password_base64
