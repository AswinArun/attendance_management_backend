from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user.id)
    if db_user:
        raise HTTPException(status_code=400, detail="id already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id:str, user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, user, user_id)

@app.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db=db, user_id=user_id)
    return {"detail": "User deleted successfully"}

@app.get("/users/instructors/")
def read_instructors(db: Session = Depends(get_db)):
    instructors =  crud.get_all_instructors(db)
    return instructors

@app.get("/users/students/")
def read_students(db: Session = Depends(get_db)):
    students = crud.get_all_students(db)
    return students

@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_code(db, code=course.code)
    if db_course:
        raise HTTPException(status_code=400, detail="course already exists")
    return crud.create_course(db=db, course=course)

@app.get("/courses")
def read_courses(db: Session = Depends(get_db)):
    return crud.get_all_courses(db)

@app.get("/courses/code/{code}")
def read_courses_by_code(code:str, db: Session = Depends(get_db)):
    return crud.get_course_by_code(db, code)

@app.get("/courses/instructor/{instructor_id}")
def read_courses_by_instructor(instructor_id:str, db: Session = Depends(get_db)):
    return crud.get_course_by_instructor(db, instructor_id)

@app.put("/courses/{course_code}", response_model=schemas.Course)
def update_course(course_code:str, course: schemas.Course, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_code(db, code=course_code)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.update_course(db, course, course_code)

@app.delete("/courses/{course_code}")
def delete_course(course_code:str, db:Session = Depends(get_db)):
    db_course = crud.get_course_by_code(db, code=course_code)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    crud.delete_course(db=db, coursecode=course_code)
    return {"detail": "Course deleted successfully"}

@app.post("/enrollments/", response_model=schemas.Enrollment)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    db_enrollment = crud.get_enrollment_by_courseandstudent(db, coursecode=enrollment.course_code, studentid=enrollment.student_id)
    if db_enrollment:
        raise HTTPException(status_code=400, detail="already enrolled")
    return crud.create_enrollment(db=db, enrollment=enrollment)

@app.get("/enrollments")
def read_enrollments(db: Session = Depends(get_db)):
    return crud.get_all_enrollments(db)

@app.get("/enrollments/code/{code}")
def read_enrollments_by_code(code:str, db: Session = Depends(get_db)):
    return crud.get_enrollment_by_course_code(db, code)

@app.get("/enrollments/student/{student_id}")
def read_enrollments_by_student(student_id:str, db: Session = Depends(get_db)):
    return crud.get_enrollment_by_student_id(db, student_id)

@app.delete("/enrollments/{enrollment_id}")
def delete_enrollment(enrollment_id:str, db:Session = Depends(get_db)):
    db_enrollment = crud.get_enrollment_by_id(db, id=enrollment_id)
    if db_enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    crud.delete_enrollment(db=db, enrollmentid=enrollment_id)
    return {"detail": "Enrollment deleted successfully"}

@app.post("/course_classes/", response_model=schemas.CourseClassCreate)
def create_course_class(course_class: schemas.CourseClassCreate, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_code(db, course_class.course_code)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    cc = crud.create_course_class(db=db, course_class=course_class)
    for enrollment in db_course.enrollments:
        # studentid:str = enrollment.student_id
        # ccid:str = cc.id
        a = schemas.AttendanceCreate(student_id=enrollment.student_id, course_class_id=cc.id)
        crud.create_attendance(db, a)
    return cc

@app.get("/course_classes/")
def read_course_classes(db: Session = Depends(get_db)):
    return crud.get_all_course_classes(db)

@app.get("/course_classes/{code}")
def read_course_classes_by_code(code:str, db: Session = Depends(get_db)):
    return crud.get_course_class_by_course_code(db, code)

@app.delete("/course_classes/{course_class_id}")
def delete_course_class(course_class_id:str, db:Session = Depends(get_db)):
    db_course_class = crud.get_course_class_by_id(db, id=course_class_id)
    if db_course_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    crud.delete_course_class(db=db, class_id=course_class_id)
    return {"detail": "Class deleted successfully"}

# @app.post("/attendance/", response_model=schemas.AttendanceCreate)
# def create_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
#     return crud.create_attendance(db=db, attendance=attendance)

@app.get("/attendance/")
def read_attendance(db: Session = Depends(get_db)):
    return crud.get_all_attendance(db)

@app.get("/attendance/student/{student_id}")
def read_attendance_by_student(student_id:str, db: Session = Depends(get_db)):
    return crud.get_attendance_by_student_id(db, student_id)

@app.get("/attendance/course_class_id/{student_id}")
def read_attendance_by_student(student_id:str, db: Session = Depends(get_db)):
    return crud.get_attendance_by_student_id(db, student_id)

@app.put("/attendance/{attendance_id}")
def update_attendance(present:bool, attendance_id:int, db: Session = Depends(get_db)):
    db_attendance = crud.get_attendance_by_id(db, attendance_id)
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return crud.update_attendance(db, attendance_id, present)

# @app.delete("/attendance/{attendance_id}")
# def delete_attendance(attendance_id:str, db:Session = Depends(get_db)):
#     db_attendance = crud.get_attendance_by_id(db, id=attendance_id)
#     if db_attendance is None:
#         raise HTTPException(status_code=404, detail="Attendance not found")
#     crud.delete_attendance(db=db, attendanceid=attendance_id)
#     return {"detail": "Attendance deleted successfully"}