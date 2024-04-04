from fastapi import APIRouter

from auth_models.sign_in_model import UserSignIn
from auth_utils.generation_fns import *
from auth_models.auth_model import Auth_Model
from file_handler.write_to_file import write_data
from auth_utils.jwt_handler import generate_signJWT
from auth_utils.verification_fns import verify_username, verify_password

router = APIRouter()


@router.post("/auth/sign_up")
def sign_up(body: Auth_Model):
    sorted_user = verify_username(body.username)
    if sorted_user:
        return {"error": "username already existed"}
    updated_db = generate_new_user_data(body)
    write_data("database/auth_users.json", updated_db)
    auth_token = generate_signJWT(body, body.user_role)
    updated_tokens = generate_new_tokens_data(body.username, auth_token)
    write_data("database/users_tokens.json", updated_tokens)
    return auth_token


@router.post("/auth/sign_in")
def sign_in(body: UserSignIn):
    sorted_user = verify_username(body.username)
    if sorted_user:
        sorted_password = sorted_user["password"]
        if verify_password(sorted_password, body.password):
            auth_token = generate_signJWT(body, sorted_user["user role"])
            updated_tokens = generate_new_tokens_data(body.username, auth_token)
            write_data("database/users_tokens.json", updated_tokens)
            if auth_token:
                return {"msg": "You signed in successfully"}
        else:
            return {"msg": "Failed to sign in ,your password is incorrect"}
    return {"msg": "Failed to sign in ,your username is incorrect"}
