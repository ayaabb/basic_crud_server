import bcrypt

from FileHandler.read_from_file import get_data

auth_users_path = "database/auth_users.json"


def generate_new_user_data(body):
    """
        Generate updated user data by adding a new user with hashed password and user role.
        param : body: The request body containing user information, including username, password, and user role.
        Returns:  dict: The updated user data with the new user added.
        """
    hashed_password = generate_hash_password(body.password)
    current_db = get_data(auth_users_path)
    current_db[body.username] = {
        "password": hashed_password,
        "user role": body.user_role
    }
    return current_db


def generate_hash_password(password):
    """
       Generate a hashed password using bcrypt.
       param: password (str): The password string to be hashed.
       Returns (str) :  The hashed password.
       """
    bytes_ = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes_, salt).decode("utf-8")
