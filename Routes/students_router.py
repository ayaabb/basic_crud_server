from fastapi import APIRouter, HTTPException, Depends

from AuthUtils.auth_utils import check_Authorization, check_if_user_admin
from FileHandler.read_from_file import get_data
from FileHandler.write_to_file import write_data
from StudentsModels.student_model import student_model
from StudentsUtils.students_utils import get_student_by_id, class_students, add_new_student_to_data, \
    delete_student_from_data
from logger.logging_decorator import log_decorator

router = APIRouter()
students_file_path = "database/students.json"


@router.get('/students')
@log_decorator
def get_all_students(payload=Depends(check_Authorization)):
    """
    Retrieve all students.
    param: request (Request): The incoming HTTP request object.
    Returns: List[student_model]: A list of all students.
    Raises: HTTPException:  If no validated token is provided for the username in the request.
    """
    try:
        if isinstance(payload, HTTPException):
            raise payload
        data = get_data(students_file_path)
        return data
    except HTTPException as e:
        status_code = e.status_code
        msg_key = "Success"
        if status_code >= 400:
            msg_key = "Error"
        return {msg_key: str(e)}


@router.get('/students/{student_id}')
@log_decorator
def get_student(student_id: int, payload=Depends(check_Authorization)):
    """
    Retrieve all students.
    param: request (Request): The incoming HTTP request object.
    Returns: List[student_model]: A list of all students.
    Raises: HTTPException:  If no validated token is provided for the username in the request.
    """
    try:
        if isinstance(payload, HTTPException):
            raise payload
        students = get_data(students_file_path)
        student = get_student_by_id(student_id, students)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        else:
            return student
    except HTTPException as e:
        status_code = e.status_code
        msg_key = "Success"
        if status_code >= 400:
            msg_key = "Error"
        return {msg_key: str(e)}


@router.get('/students/classes/{class_name}')
@log_decorator
def get_class_students(class_name: str, is_admin=Depends(check_if_user_admin)):
    """
    Retrieve students belonging to a specific class.
    parma: class_name (str): The name of the class to filter students by.
    Returns: A list of names of students belonging to the specified class.
            If class not found, returns {"error msg": "class not found"}.
    Raises: HTTPException: If no validated token is provided for the username in the request, or if the user is not authorized as an admin.
    """

    try:
        if isinstance(is_admin, HTTPException):
            raise is_admin
        students = get_data(students_file_path)
        list_students = class_students(class_name, students)
        if len(list_students) == 0:
            raise HTTPException(status_code=404, detail="Class not found")
        return list_students

    except HTTPException as e:
        status_code = e.status_code
        msg_key = "Success"
        if status_code >= 400:
            msg_key = "Error"
        return {msg_key: str(e)}


@router.post("/students/add_student")
@log_decorator
def add_student(body: student_model, is_admin=Depends(check_if_user_admin)):
    """
     Add a new student to the database.
     param: request (Request): The incoming HTTP request object.
         body (student_model): The data for the new student.
     Returns: student_model: The added student data.
     Raises: HTTPException: If no validated token is provided for the username in the request, or if the user is not authorized as an admin.

     """
    try:
        if isinstance(is_admin, HTTPException):
            raise is_admin
        new_data = add_new_student_to_data(body.name, body.id_, body.age, body.classes, students_file_path)
        write_data(students_file_path, new_data)
        raise HTTPException(status_code=200, detail="added student successfully")
    except HTTPException as e:
        status_code = e.status_code
        msg_key = "Success"
        if status_code >= 400:
            msg_key = "Error"
        return {msg_key: str(e)}


@router.delete("/students/delete_all_students")
@log_decorator
def delete_all_students(is_admin=Depends(check_if_user_admin)):
    try:
        if isinstance(is_admin, HTTPException):
            raise is_admin
        write_data(students_file_path, [])
        raise HTTPException(status_code=200, detail="deleted all students successfully")
    except HTTPException as e:
        status_code = e.status_code
        msg_key = "Success"
        if status_code >= 400:
            msg_key = "Error"
        return {msg_key: str(e)}


@router.delete("/students/delete_student/{student_id}")
@log_decorator
def delete_student(student_id: int, payload=Depends(check_Authorization)):
    try:
        if isinstance(payload, HTTPException):
            raise payload
        students = get_data(students_file_path)
        updated_data = delete_student_from_data(student_id, students)
        if updated_data is None:
            raise HTTPException(status_code=404, detail="Student not found")
        else:
            write_data(students_file_path, updated_data)
            raise HTTPException(status_code=200, detail="deleted student successfully")

    except HTTPException as e:
        status_code = e.status_code
        msg_key = "Success"
        if status_code >= 400:
            msg_key = "Error"
        return {msg_key: str(e)}
