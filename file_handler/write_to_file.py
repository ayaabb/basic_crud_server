import json


def write_data(file_path, new_data):
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(new_data, file)
