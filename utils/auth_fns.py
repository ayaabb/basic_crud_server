import time

import bcrypt
import jwt
from decouple import config

from file_handler.read_from_file import get_data

auth_users_path = "database/auth_users.json"
users_tokens_path = "database/users_tokens.json"
JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def prepare_new_tokens_data(username, token):
    current_db = get_data(users_tokens_path)
    current_db[username] = token
    return current_db


def prepare_new_user_data(body):
    hashed_password = hash_password(body.password)
    current_db = get_data(auth_users_path)
    current_db[body.username] = {
        "password": hashed_password,
        "user role": body.user_role
    }
    return current_db


def hash_password(password):
    bytes_ = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes_, salt).decode("utf-8")


def check_username(username):
    users = get_data(auth_users_path)
    if username in users.keys():
        return users[username]
    return None


def verify_password(sorted_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), sorted_password.encode('utf-8'))


def token_response(token: str):
    return {
        "access token": token
    }


def generate_signJWT(body, role):
    payload = {
        "user role": role,
        "username": body.username,
        "expiry": time.time() + 100
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def check_Authorization(request):
    auth_header_user_name = request.headers.get('Authorization')
    if auth_header_user_name:
        if check_username(auth_header_user_name):
            tokens = get_data(users_tokens_path)
            return verify_jwt(tokens[auth_header_user_name]["access token"])
    return None


def verify_jwt(token):
    decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    return decode_token if decode_token["expiry"] >= time.time() else None


def check_if_user_admin(request):
    auth_header_user_name = request.headers.get('Authorization')
    return check_username(auth_header_user_name)["user role"] == "admin"
