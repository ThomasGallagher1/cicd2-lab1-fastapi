from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, StringConstraints

NameStr = Annotated[str,StringConstraints(min_length = 2, max_length=50)]
StduentidStr = Annotated[str, StringConstraints(pattern=r"^S\d{7}$")]

class UserCreate(BaseModel):
    name: NameStr
    email: EmailStr
    age: int = Field(gt=18, lt=120)
    student_id: Annotated[str, StringConstraints(pattern=r"^S\d{7}$")] 

class UserRead(BaseModel):
    id: int
    name: NameStr
    email: EmailStr
    age: int = Field(gt=18, lt=120)
    student_id: Annotated[str, StringConstraints(pattern=r"^S\d{7}$")] 