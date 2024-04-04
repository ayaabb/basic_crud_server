import time

import jwt

from file_handler.read_from_file import get_data
from auth_utils.verification_fns import verify_username

JWT_SECRET = "831809585cd154b09a6b1648c1bb7eee"
JWT_ALGORITHM = "HS256"
users_tokens_path = "database/users_tokens.json"


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
        if verify_username(auth_header_user_name):
            tokens = get_data(users_tokens_path)
            return verify_jwt(tokens[auth_header_user_name]["access token"])
    return None


def verify_jwt(token):
    decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    return decode_token if decode_token["expiry"] >= time.time() else None


def check_if_user_admin(request):
    auth_header_user_name = request.headers.get('Authorization')
    return verify_username(auth_header_user_name)["user role"] == "admin"
