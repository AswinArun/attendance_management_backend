from pydantic import BaseModel
from datetime import datetime

class AttendanceBase(BaseModel):
    student_id: str
    course_class_id:int

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id:int
    present:bool = False
    
    class Config:
        orm_mode = True

class CourseClassBase(BaseModel):
    date_time: datetime
    course_code: str

class CourseClassCreate(CourseClassBase):
    pass

class CourseClass(CourseClassBase):
    id:int
    attendance: list[Attendance] = []

    class Config:
        orm_mode = True

class EnrollmentBase(BaseModel):
    student_id: str
    course_code:str

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id:int

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    instructor_id: str
    code: str
    title: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    enrollments: list[Enrollment] = []
    course_classes: list[CourseClass] = []

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    user_id: str

class StudentCreate(BaseModel):
    pass

class Student(StudentBase):
    id:int
    enrollments: list[Enrollment] = []
    attendance: list[Attendance] = []

    class Config:
        orm_mode = True


class InstructorBase(BaseModel):
    user_id: str

class InstructorCreate(InstructorBase):
    pass

class Instructor(InstructorBase):
    id:int
    courses: list[Course] = []
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    id: str
    role: str
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):

    class Config:
        orm_mode = True