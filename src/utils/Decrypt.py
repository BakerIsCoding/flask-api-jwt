import sqlite3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
import base64
import os

def decrypt_password(encrypted_password):
    secret_key = os.environ.get('SECRET_KEY')
    
    # Generar un hash SHA-512 de la clave secreta
    hashed_key = hashlib.sha512(secret_key.encode()).digest()

    # Utilizar el primer bloque de 16 bytes del hash como clave AES
    aes_key = hashed_key[:16]
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(b'\0' * 16), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decodificar la contraseña cifrada desde base64
    encrypted_password_bytes = base64.b64decode(encrypted_password)
    decrypted_password = decryptor.update(encrypted_password_bytes) + decryptor.finalize()

    # Eliminar el relleno y convertir a cadena
    decrypted_password_str = decrypted_password.rstrip(b'\0').decode()

    return decrypted_password_str

