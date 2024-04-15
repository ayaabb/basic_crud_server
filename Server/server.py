from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
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


@school.middleware("http")
async def log_req(request: Request, call_next):
    print(f'got req. to: {request.url}, method: {request.method}')
    response = await call_next(request)
    x = 1
    if x == 1:
        return response
    return JSONResponse(content={"error": "Unauthorized"}, status_code=401)




