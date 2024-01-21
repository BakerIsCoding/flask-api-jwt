from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
import base64
import os

def encryptPassword(password):
    secretKey = os.environ.get('SECRET_KEY')
    
    # Generar un hash SHA-512 de la clave secreta
    hashedKey = hashlib.sha512(secretKey.encode()).digest()
    aesKey = hashedKey[:16]
    cipher = Cipher(algorithms.AES(aesKey), modes.CBC(b'\0' * 16), backend=default_backend())
    encryptor = cipher.encryptor()

    # Rellenar la contraseña para que tenga una longitud múltiplo de 16
    passwordPadded = password.ljust((len(password) // 16 + 1) * 16)
    encryptedPassword = encryptor.update(passwordPadded.encode()) + encryptor.finalize()
    encryptedPasswordBase64 = base64.b64encode(encryptedPassword).decode()

    return encryptedPasswordBase64
