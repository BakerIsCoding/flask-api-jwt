import sqlite3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
import base64
import os

def decryptPassword(encrypted_password):
    
    secretKey = os.environ.get('SECRET_KEY')
    hashedKey = hashlib.sha512(secretKey.encode()).digest()

    # Utilizar el primer bloque de 16 bytes del hash como clave AES
    aesKey = hashedKey[:16]
    cipher = Cipher(algorithms.AES(aesKey), modes.CBC(b'\0' * 16), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decodificar la contraseña cifrada desde base64
    encryptedPasswordBytes = base64.b64decode(encrypted_password)
    decryptedPassword = decryptor.update(encryptedPasswordBytes) + decryptor.finalize()

    # Eliminar el relleno y convertir a cadena
    decryptedPasswordStr = decryptedPassword.rstrip(b'\0').decode()

    return decryptedPasswordStr

