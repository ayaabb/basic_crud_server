from file_handler.read_from_file import get_data


def generate_new_student_data(name, id_, age, classes,file_path):
    data = get_data(file_path)
    data.append({"name": name, "id": id_, "age": age, "classes": classes})
    return data

def class_students(class_name,students):
    list_students = []
    for student in students:
        if class_name in student["classes"]:
            list_students.append(student["name"])
    return list_students


def get_student_by_id(student_id,students):
    for student in students:
        if student["id"] == str(student_id):
            return student["name"]
    return None

