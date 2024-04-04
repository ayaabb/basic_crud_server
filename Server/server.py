from fastapi import FastAPI
from Routes import students_router, auth_router

"""
FastAPI instance representing the school's API.
Includes routers for authentication and student-related endpoints.
Attributes:
    auth_router (APIRouter): Router for authentication endpoints.
    students_router (APIRouter): Router for student-related endpoints.
"""

school = FastAPI()

school.include_router(auth_router.router)
school.include_router(students_router.router)
