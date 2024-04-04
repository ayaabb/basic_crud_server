import json


def write_data(file_path, new_data):
    """
       Write data to a JSON file.
       param: file_path (str): The file path of the JSON file to write to.
           new_data (dict): The data to be written to the JSON file.
       """
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(new_data, file)
