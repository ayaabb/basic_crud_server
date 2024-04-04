from pydantic import BaseModel


class UserSignIn(BaseModel):
    """
        Pydantic model representing user sign-in data.
    """
    username: str
    password: str
