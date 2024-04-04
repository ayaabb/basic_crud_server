from fastapi import APIRouter, Request, HTTPException
from file_handler.read_from_file import get_data
from file_handler.write_to_file import write_data
from models.student_model import student_model
from utils.auth_fns import check_Authorization, check_if_user_admin
from utils.students_fns import generate_new_student_data, class_students, get_student_by_id

router = APIRouter()


@router.get('/students')
async def get_all_students(request: Request):
    """
    Retrieve all students.
    Returns: List: A list of all students.
    """
    request_auth = check_Authorization(request)
    if request_auth:
        return get_data("database/students.json")

    else:
        raise HTTPException(400, "no token")


@router.get('/students/{student_id}')
async def get_student(request: Request, student_id: int):
    """ Retrieve a specific student by his id
        param: student_id (int): The id of the student to retrieve.
        Returns: str: The name of the student if found, otherwise "student not found".
    """
    request_auth = check_Authorization(request)
    if request_auth:
        students = get_data("database/students.json")
        student = get_student_by_id(student_id, students)
        return {"error msg": "student not found"} if not student else student

    else:
        raise HTTPException(400, "no token")


@router.get('/students/classes/{class_name}')
async def get_class_students(request: Request, class_name: str):
    """Retrieve students belonging to a specific class.
    param: class_name (str): The name of the class to filter students by.
    Returns: List: A list of names of students belonging to the specified class.
              If class not found, returns "class not found".
    """
    request_auth = check_Authorization(request)
    if request_auth:
        if check_if_user_admin(request):
            students = get_data("database/students.json")
            list_students = class_students(class_name, students)
            if len(list_students) == 0:
                return {"error msg": "class not found"}
            return list_students
        else:
            raise HTTPException(400, "not allowed")
    else:
        raise HTTPException(400, "no token")


@router.post("/students/add_student")
async def add_student(request: Request, body: student_model):
    """
    Add a new student to the database.
    param: body (student_model): The data for the new student.
    Returns: student_model: The added student data.
    """

    request_auth = check_Authorization(request)
    if request_auth:
        if check_if_user_admin(request):
            new_data = generate_new_student_data("database/students.json", body.name, body.id_, body.age, body.classes)
            write_data("database/students.json", new_data)
            return body
        else:
            raise HTTPException(400, "not allowed")
    else:
        raise HTTPException(400, "no token")