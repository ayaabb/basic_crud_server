from pydantic import BaseModel


class UserSignUp(BaseModel):
    """
        Pydantic model representing user sign-up data.
    """
    username: str
    password: str
    user_role: str

