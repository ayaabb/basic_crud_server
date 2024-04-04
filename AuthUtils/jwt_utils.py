import time

import jwt

from AuthUtils.token_utils import token_response

JWT_SECRET = "831809585cd154b09a6b1648c1bb7eee"
JWT_ALGORITHM = "HS256"


def verify_jwt(token):
    """
        Verify a JWT token.
        param: token (str): The JWT token to verify.
        Returns: dict or None: If the token is valid and not expired, returns the decoded token.
                         If the token is invalid or expired, returns None.
        """
    decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    return decode_token if decode_token["expiry"] >= time.time() else None


def generate_signJWT(body, role):
    """
       Generates a signed JWT token based on the user role , the username and the expiry time of the token (100 seconds after generation).
       param: body: The request body containing user information.
           role (str): The role of the user.
       Returns: dict: A dictionary containing the access token.
       """
    payload = {
        "user role": role,
        "username": body.username,
        "expiry": time.time() + 100
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)
