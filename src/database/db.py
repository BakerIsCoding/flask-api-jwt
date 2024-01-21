from decouple import config
from src.utils.errors.CustomException import CustomException
import pymysql


def get_connection():
    try:
        return pymysql.connect(
            host=config('MYSQL_HOST'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            db=config('MYSQL_DB')
        )
    except CustomException as ex:
        raise CustomException(ex)


def getUserById(userId):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM user WHERE id = %s"
        cursor.execute(query, (userId,))
        user = cursor.fetchone()
        return user
    except CustomException as ex:
        raise CustomException(ex)
    
def getUserByUsername(username):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        return user
    except CustomException as ex:
        raise CustomException(ex)
    
def getAllUsers():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM user"
        cursor.execute(query)
        users = cursor.fetchall()
        return users
    except CustomException as ex:
        raise CustomException(ex)
    
def updateUser(user):
    try:
        ##User params: id, username, password, email, isadmin
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE user SET username = %s, password = %s, email = %s, isadmin = %s WHERE id = %s"
        cursor.execute(query, (user.username, user.password, user.email, user.isadmin, user.id))
        connection.commit()
        connection.close()
        return True
    except CustomException as ex:
        raise CustomException(ex)

def deleteUser(id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM user WHERE id = %s"
        cursor.execute(query, (id))
        connection.commit()
        connection.close()
        return True
    except CustomException as ex:
        raise CustomException(ex)