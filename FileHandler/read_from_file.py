import json


def get_data(file_path):
    """
        Retrieve data from a JSON file.
        para: file_path (str): The file path of the JSON file to read.
        Returns: dict: The data read from the JSON file.
        """
    print(file_path)
    with open(file_path, "r") as file:
        data = json.load(file)

    return data


