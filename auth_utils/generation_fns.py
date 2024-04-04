import bcrypt

from file_handler.read_from_file import get_data

auth_users_path = "database/auth_users.json"
users_tokens_path = "database/users_tokens.json"

def generate_new_tokens_data(username, token):
    current_db = get_data(users_tokens_path)
    current_db[username] = token
    return current_db


def generate_new_user_data(body):
    hashed_password = generate_hash_password(body.password)
    current_db = get_data(auth_users_path)
    current_db[body.username] = {
        "password": hashed_password,
        "user role": body.user_role
    }
    return current_db


def generate_hash_password(password):
    bytes_ = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes_, salt).decode("utf-8")


