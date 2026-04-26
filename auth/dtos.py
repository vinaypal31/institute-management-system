from pydantic import BaseModel , EmailStr , Field
from typing import Optional
from datetime import date

class Register(BaseModel):

    email: EmailStr
    password: str = Field(min_length=6, max_length=20)

class Login(BaseModel):

    email: EmailStr
    password: str= Field(min_length=6, max_length=20)

class TeacherUpsert(BaseModel):

    teacher_id: Optional[int] = None
    name: str

class AttendanceCreate(BaseModel):
    student_id: int
    course_id: int
    date: date
    status: str  # present / absent

class AttendanceResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    date: date
    status: str

    class Config:
        from_attributes = True