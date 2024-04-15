from FileHandler.read_from_file import get_data


def delete_student_from_data(student_id, students):
    for student in students:
        if student['id'] == student_id:
            students.remove(student)
            return students
    return None


def add_new_student_to_data(name, id_, age, classes, file_path):
    """
         Add a new student to the existing data.
         param: name (str): The name of the new student.
            id_ (str): The id of the new student.
            age (int): The age of the new student.
            classes (List[str]): A list of classes the new student is enrolled in.
            file_path (str): The file path of the JSON file containing the students' data.
        Returns: The updated students data containing the new student.
        """
    data = get_data(file_path)
    data.append({"name": name, "id": id_, "age": age, "classes": classes})
    return data


def class_students(class_name, students):
    """
    Retrieve a list of students belonging to a specific class.
    param: class_name (str): The name of the class to filter students by.
        students : A list of dictionaries representing student data.
    Returns: List[str]: A list of names of students belonging to the specified class.
    """
    list_students = []
    for student in students:
        if class_name in student["classes"]:
            list_students.append(student["name"])
    return list_students


def get_student_by_id(student_id, students):
    """
        Retrieve the name of a student by his id.
        param: student_id (str): The id of the student to retrieve.
            students : A list of dictionaries representing student data.
        Returns: The name of the student if found, otherwise None.
        """
    for student in students:
        if student["id"] == student_id:
            return student["name"]
    return None
