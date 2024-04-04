from typing import List

from pydantic import BaseModel


class student_model(BaseModel):
    """
     Pydantic model representing a student.
    """
    name: str
    id_: int
    age: int
    classes: List[str]
