from flask import Blueprint, request, jsonify

# Models
from src.services.models.User import User
# Utils
from src.utils.Security import Security
from src.utils.Encrypt import encryptPassword
# Services
from src.services.AuthService import AuthService, RegisterService


main = Blueprint('auth_blueprint', __name__)


@main.route('/login', methods=['POST'])
def login():
    username = None
    password = None
    try:
        username = request.json['username']
        password = request.json['password']

        _user = User(0, username, password, None, None)
        authenticated_user = AuthService.login_user(_user)
        print(authenticated_user.isadmin)
        if (authenticated_user != None):
            print(authenticated_user.isadmin)
            encoded_token = Security.generate_token(authenticated_user)
            return jsonify({'success': True, 'token': encoded_token})
        else:
            response = jsonify({'success': False, 'message': 'Unauthorized'})
            return response, 401
    except Exception as ex:
        if username == None:
            response = jsonify({'success': False, 'message': 'The field "username" is required'})
            return response, 400
        elif password == None:
            response = jsonify({'success': False, 'message': 'The field "password" is required'})
            return response, 400
        else:
            response = jsonify({'success': False, 'message': 'Error trying to login, error: ' + str(ex)})
            return response, 500

@main.route('/register', methods=['POST'])
def register():
    username = None
    password = None
    email = None
    try:
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        encryptedPassword = encryptPassword(password)
        
        user = User(0, username, encryptedPassword, email, 0)
        userRegisted = RegisterService.registerUser(user)
        
        if (userRegisted == 0):
            return jsonify({'success': False, 'message': 'Something went wrong trying to register a new user'})
        
        elif (userRegisted == 1):
            return jsonify({'success': True})
        
        else:
            response = jsonify({'success': False, 'message': 'The user ' + username + ' already exists'})
            return response, 500
        
    except Exception as ex:
        if username == None:
            response = jsonify({'success': False, 'message': 'The field "username" is required'})
            return response, 400
        elif password == None:
            response = jsonify({'success': False, 'message': 'The field "password" is required'})
            return response, 400
        elif email == None:
            response = jsonify({'success': False, 'message': 'The field "email" is required'})
            return response, 400
        else:
            response = jsonify({'success': False, 'message': 'Error trying to register a new user, error: ' + str(ex)})
            return response, 500
        
