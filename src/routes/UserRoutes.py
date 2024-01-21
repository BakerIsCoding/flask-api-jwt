from flask import Blueprint, request, jsonify

# Models
from src.services.models.User import User
# Security
from src.utils.Decrypt import decryptPassword
from src.utils.Encrypt import encryptPassword
from src.utils.Security import Security
# Services
from src.services.AuthService import AuthService
#Db
from src.database.db import getUserById as getUserByIdDb
from src.database.db import getAllUsers as getAllUsersDb
from src.database.db import updateUser as updateUserDb
from src.database.db import deleteUser as deleteUserDb
from src.utils import UtilsFile as Utils

main = Blueprint('user_blueprint', __name__)

#ENDPOINT /API/USER
@main.route("/<int:id>", methods=["GET"])
def getUserById(id):
    has_access = Security.verifyAdminToken(request.headers)
    if has_access:
        try:
            dbUser = getUserByIdDb(id)
            if dbUser is not None:
                user = User(dbUser[0], dbUser[1], None, dbUser[3], dbUser[4])
                print(dbUser)
                return jsonify({'user': {'id': user.id, 'username': user.username, 'email': Utils.bytesToString(user.email), "isadmin": user.isadmin}, 'success': True})

            else:
                return jsonify({'message': "User Not Found", 'success': False})
        except Exception as ex:
            return jsonify({'message': f"ERROR: {str(ex)}", 'success': False})

    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

@main.route("/all")
def getAllUsers():
    has_access = Security.verifyAdminToken(request.headers)
    if has_access:
        try:
            users = getAllUsersDb()
            allUsers = []
            for user in users:
                allUsers.append({"id": user[0], "username": user[1], "email": Utils.bytesToString(user[3]), "isadmin": user[4]})
            return jsonify({'users': allUsers, 'success': True})
        except Exception as ex:
            return jsonify({'message': f"ERROR: {str(ex)}", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized', 'isadmin': False, 'success': False})
        return response, 401


@main.route("/delete/<int:id>", methods=["POST"])
def deleteUser(id):
    has_access = Security.verifyAdminToken(request.headers)
    if has_access:
        try:
            deleteUserFromDb = deleteUser(id)
            if deleteUserFromDb:
                    return jsonify({'message': f"User with id '"+ id +"' deleted", 'success': True})
            else:
                return jsonify({'message': "User Not Found", 'success': False})
        except Exception as ex:
            return jsonify({'message': f"ERROR: {str(ex)}", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

## ENDPOINT /API/USER/UPDATE/<ID>
## PARAMS: ID, USERNAME, PASSWORD, EMAIL, ISADMIN
## UPDATE USER BY ID

@main.route("/update/<int:id>", methods=["POST"])
def updateUser(id):
    has_access = Security.verifyAdminToken(request.headers)
    if has_access:
        try:
            username = request.json['username']
            password = request.json['password']
            email = request.json['email']
            isadmin = request.json['isadmin']
            dbUser = getUserByIdDb(id)
            
            if request.json['username'] == "":
                username = dbUser[1]
            if request.json['password'] == "":
                password = decryptPassword(dbUser[2])
            if request.json['email'] == "":
                email = dbUser[3]
            if request.json['isadmin'] == "":
                isadmin = dbUser[4]
            
            encryptedPassword = encryptPassword(password)
            
            user = User(id, username, encryptedPassword, email, isadmin)
            updateUserFromDb = updateUserDb(user)
            if updateUserFromDb:
                    return jsonify({'message': f"User with id '"+ id +"' updated", 'success': True})
            else:
                return jsonify({'message': "User Not Found", 'success': False})
        except Exception as ex:
            return jsonify({'message': f"ERROR: {str(ex)}", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    
    
