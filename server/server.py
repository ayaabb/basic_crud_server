from fastapi import FastAPI
from routes import students_router, auth_router

school = FastAPI()

school.include_router(auth_router.router)
school.include_router(students_router.router)
