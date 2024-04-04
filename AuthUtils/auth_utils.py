import bcrypt

from AuthUtils.jwt_utils import verify_jwt
from FileHandler.read_from_file import get_data

auth_users_path = "database/auth_users.json"
users_tokens_path = "database/users_tokens.json"


def check_Authorization(request):
    """
        Check the authorization header in the request and verify the JWT token.
        param: request: The incoming HTTP request object.
        Returns: dict or None: If the JWT token is valid, returns the decoded token.
                         If the token is invalid or missing, returns None.
        """
    auth_header_user_name = request.headers.get('Authorization')
    if auth_header_user_name:
        if verify_username(auth_header_user_name):
            tokens = get_data(users_tokens_path)
            return verify_jwt(tokens[auth_header_user_name]["access token"])
    return None


def check_if_user_admin(request):
    """
       Check if the user is an admin based on the authorization header in the request.
       param: request: The incoming HTTP request object.
       Returns: bool: True if the user is an admin, False otherwise.
       """
    auth_header_user_name = request.headers.get('Authorization')
    return verify_username(auth_header_user_name)["user role"] == "admin"


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
