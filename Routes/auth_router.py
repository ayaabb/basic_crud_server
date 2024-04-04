from fastapi import APIRouter

from AuthModels.auth_model import UserSignUp
from AuthModels.sign_in_model import UserSignIn
from AuthUtils.auth_utils import *
from AuthUtils.jwt_utils import generate_signJWT
from FileHandler.write_to_file import write_data
from AuthUtils.token_utils import generate_new_tokens_data
from AuthUtils.user_utils import generate_new_user_data

router = APIRouter()


@router.post("/auth/sign_up")
def sign_up(body: UserSignUp):
    """
    Register a new user.
    param: body (Auth_Model): The user data including username, password, and user role.
    Returns: str: Authentication token if sign-up is successful. Returns {"error": "username already existed"}
             if the username already exists in the database.
    """
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
    """
        Authenticate an existing user.
        param: body (UserSignIn): The user data including username and password.
        Returns:   dict: Returns {"msg": "You signed in successfully"} if sign-in is successful.
                  Returns {"msg": "Failed to sign in, your password is incorrect"} if the password is incorrect.
                  Returns {"msg": "Failed to sign in, your username is incorrect"} if the username is incorrect.
        """
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
