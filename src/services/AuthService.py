# Database
from src.database.db import get_connection, getUserByUsername
# Errors
from src.utils.errors.CustomException import CustomException
# Models
from .models.User import User

from src.utils.Decrypt import decrypt_password


class AuthService():

    @classmethod
    def login_user(cls, user):
        try:
            #connection = get_connection()
            authenticated_user = None
            entityUser = getUserByUsername(user.username)
            
            dbDecryptedPass = decrypt_password(entityUser[2]).strip()
            print(entityUser[4])
            if dbDecryptedPass == user.password.strip():
                print(entityUser[4])
                authenticated_user = User(
                    entityUser[0], entityUser[1], None, entityUser[3], entityUser[4])
                if entityUser[4] == 1:
                    authenticated_user.isadmin = True
            return authenticated_user
            
        except CustomException as ex:
            print("error en auth service")
            raise CustomException(ex)




class RegisterService():

    @classmethod
    def registerUser(cls, user):
        # Return codes:
        # 0 = Internal error
        # 1 = Success
        # 2 = User already exists
        try:
            connection = get_connection()
            userRegisted = 0
            userFromDb = getUserByUsername(user.username)
            print(userFromDb)
            
            if userFromDb is not None:
                userRegisted = 2
                return userRegisted
            
            with connection.cursor() as cursor:
                query = "INSERT INTO user (username, password, email, isadmin) VALUES (%s, %s, %s, %s)"
                cursor.execute(
                    query, (user.username, user.password, user.email, user.isadmin))
                connection.commit()
                connection.close()
                userRegisted = 1
            return userRegisted
        except CustomException as ex:
            return userRegisted
            
