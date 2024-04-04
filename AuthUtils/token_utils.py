from FileHandler.read_from_file import get_data

users_tokens_path = "database/users_tokens.json"


def token_response(token):
    """
       Generates a response containing the access token.
       param: token (str): The access token.
       Returns: dict: A dictionary containing the access token.
       """
    return {
        "access token": token
    }


def generate_new_tokens_data(username, token):
    """
        Generate updated user tokens data by adding a new token for the specified username.
        param: username (str): The username for which the token is generated.
            token (str): The token to be associated with the username.
        Returns: dict: The updated users tokens data with the new token added.
        """
    current_db = get_data(users_tokens_path)
    current_db[username] = token
    return current_db
