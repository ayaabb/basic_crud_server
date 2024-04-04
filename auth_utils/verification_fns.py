import bcrypt

from file_handler.read_from_file import get_data

auth_users_path = "database/auth_users.json"


def verify_username(username):
    users = get_data(auth_users_path)
    if username in users.keys():
        return users[username]
    return None


def verify_password(sorted_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), sorted_password.encode('utf-8'))


