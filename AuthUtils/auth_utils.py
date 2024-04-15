import bcrypt
from fastapi import Depends, Request, HTTPException

from AuthUtils.jwt_utils import verify_jwt
from FileHandler.read_from_file import get_data

auth_users_path = "database/auth_users.json"
users_tokens_path = "database/users_tokens.json"


def check_Authorization(request: Request):
    """
        Check the authorization header in the request and verify the JWT token.
        param: request: The incoming HTTP request object.
        Returns: dict : If the JWT token is valid, returns the decoded token,
         HTTPException: If the user doesn't have valid token returns an HTTPException.
        """
    try:
        auth_header_user_name = request.headers.get('Authorization')
        if auth_header_user_name:
            if verify_username(auth_header_user_name):
                tokens = get_data(users_tokens_path)
                is_token_validated = verify_jwt(tokens[auth_header_user_name]["access token"])
                if is_token_validated is not None:
                    return is_token_validated
        raise HTTPException(status_code=401, detail="User unauthorized")
    except HTTPException as e:
        return e


def check_if_user_admin(payload=Depends(check_Authorization)):
    """
     Check if the user is an admin based on the payload from the authorization.
     Param: payload: The payload returned from the authorization check.
     Returns: bool: True if the user is an admin ,
         HTTPException: If the payload is an HTTPException, it is raised.
     """
    try:

        if isinstance(payload, HTTPException):
            raise payload
        if payload["user role"] != "admin":
            raise HTTPException(status_code=403, detail="You are not allowed!")
    except HTTPException as e:
        return e
    return True


def verify_username(username):
    """
     Verify if a username exists in the authentication database.
     param:  username (str): The username to verify.
     Returns: dict or None: If the username exists, returns the user data dictionary from the authentication database.
                       If the username doesn't exist, returns None.
     """
    users = get_data(auth_users_path)
    if username in users.keys():
        return users[username]
    return None


def verify_password(sorted_password, user_password):
    """
     Verify if a password matches the hashed password stored in the authentication database.
     param: sorted_password (str): The hashed password retrieved from the database.
         user_password (str): The user-provided password to verify.
     Returns: bool: True if the password matches the hashed password, False otherwise.
     """
    return bcrypt.checkpw(user_password.encode('utf-8'), sorted_password.encode('utf-8'))
