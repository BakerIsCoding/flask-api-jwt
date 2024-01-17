from flask import Blueprint, request, jsonify

# Models
from src.services.models.User import User
# Security
from src.utils.Security import Security
# Services
from src.services.AuthService import AuthService
#Db
from src.database.db import getUserById as getUserByIdDb
from src.database.db import getAllUsers as getAllUsersDb
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
    
    users = getAllUsersDb()
    singleUser = []
    for user in users:
        unhashed_password = str(user[0].password)
        singleUser.append(
            {"id": user[0].id, "username": user[0].username, "email": user[0].email, "password": unhashed_password,
             "isadmin": user[0].isadmin})
    return jsonify(singleUser)

    
