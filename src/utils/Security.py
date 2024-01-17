from decouple import config

from src.database.db import getUserByUsername
from src.services.models.User import User

import datetime
import jwt
import pytz
import os


class Security():

    secret = config('SECRET_KEY')
    tz = pytz.timezone("Europe/Madrid")

    @classmethod
    def generate_token(cls, authenticated_user):
        issuedAt = datetime.datetime.now(tz=cls.tz).isoformat()
        expirationTime = (datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=int(os.environ.get('TOKEN_EXPIRATION')))).isoformat()

        payload = {
            'issuedAt': issuedAt,
            'expirationTime': expirationTime,
            'id': authenticated_user.id,
            'username': authenticated_user.username,
            'isadmin': authenticated_user.isadmin
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")

    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
                    role = payload['isadmin']
                    
                    currentTime = datetime.datetime.now(tz=cls.tz)
                    expirationTime = datetime.datetime.fromisoformat(payload['expirationTime'])
                    
                    if currentTime > expirationTime:
                        return False

                    if role == 0:
                        return True
                    return False
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False

        return False
    
    @classmethod
    def verifyAdminToken(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
                    role = payload['isadmin']
                    
                    currentTime = datetime.datetime.now(tz=cls.tz)
                    expirationTime = datetime.datetime.fromisoformat(payload['expirationTime'])
                    
                    if currentTime > expirationTime:
                        return False

                    if role == 1:
                        return True
                    return False
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False

        return False
