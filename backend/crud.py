from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_

from . import models, schemas


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_users_by_role(db: Session, role:str):
    return db.query(models.User).filter(models.User.role == role).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.flush()
    db.commit()
    db.refresh(db_user)

    if (db_user.role == "instructor"):
        db_instructor = models.Instructor(user_id = db_user.id)
        db.add(db_instructor)
        db.commit()
    if (db_user.role == "student"):
        db_student = models.Student(user_id = db_user.id)
        db.add(db_student)
        db.commit()

    return db_user

def update_user(db: Session, user: schemas.User, user_id: str):
    user_to_update = db.query(models.User).filter(models.User.id == user_id).first()
    user_to_update.id = user.id
    user_to_update.role = user.role
    user_to_update.name = user.name
    db.flush()
    db.commit()
    return user_to_update

def delete_user(db: Session, user_id:str):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    # Delete the user object, triggering cascading deletes
    db.delete(user)
    db.flush()
    db.commit()

def get_all_instructors(db:Session):
    return db.query(models.User).filter(models.User.role=="instructor").all()

def get_all_students(db:Session):
    return db.query(models.User).filter(models.User.role=="student").all()

# def get_all_instructors(db: Session):
#     return db.query(models.Instructor).all()

# def get_instructor_by_user_id(db: Session, userid:str):
#     return db.query(models.Instructor).filter_by(user_id=userid).first()

def get_all_courses(db: Session):
    return db.query(models.Course).all()

def get_course_by_code(db: Session, code:str):
    return db.query(models.Course).filter(models.Course.code==code).first()

def get_course_by_instructor(db: Session, instructor_id:str):
    return db.query(models.Course).filter(models.Course.instructor_id==instructor_id).all()

def create_course(db: Session, course: schemas.CourseCreate):
    new_course = models.Course(**course.model_dump())
    db.add(new_course)
    db.flush()
    db.commit()
    db.refresh(new_course)
    return new_course

def update_course(db: Session, course: schemas.Course, course_code:str):
    course_to_update = db.query(models.Course).filter(models.Course.code==course_code).first()
    course_to_update.code = course.code
    course_to_update.title = course.title
    course_to_update.instructor_id = course.instructor_id
    db.flush()
    db.commit()
    return course_to_update

def delete_course(db: Session, coursecode: str):
    db.delete(db.query(models.Course).filter(models.Course.code==coursecode).first())
    db.flush()
    db.commit()

def get_all_enrollments(db: Session):
    return db.query(models.Enrollment).all()

def get_enrollment_by_id(db:Session, id:str):
    return db.query(models.Enrollment).filter(models.Enrollment.id==id).first()

def get_enrollment_by_student_id(db: Session, studentid: str):
    return db.query(models.Enrollment).filter(models.Enrollment.student_id==studentid).all()

def get_enrollment_by_course_code(db: Session, coursecode: str):
    return db.query(models.Enrollment).filter(models.Enrollment.course_code==coursecode).all()

def get_enrollment_by_courseandstudent(db:Session, coursecode: str, studentid:str):
    enrollments = db.query(models.Enrollment).filter(and_(models.Enrollment.course_code==coursecode, models.Enrollment.student_id==studentid)).first()
    return enrollments

def create_enrollment(db: Session, enrollment: schemas.EnrollmentCreate):
    new_enrollment = models.Enrollment(**enrollment.model_dump())
    db.add(new_enrollment)
    db.commit()
    db.flush()
    return new_enrollment

def delete_enrollment(db: Session, enrollmentid):
    db.delete(db.query(models.Enrollment).filter(models.Enrollment.id==enrollmentid).first())
    db.flush()
    db.commit()

def get_all_course_classes(db: Session):
    return db.query(models.CourseClass).all()

def get_course_class_by_id(db: Session, id:str):
    return db.query(models.CourseClass).filter(models.CourseClass.id==id)

def get_course_class_by_course_code(db:Session, coursecode: str):
    return db.query(models.CourseClass).filter(models.CourseClass.course_code==coursecode)

def create_course_class(db: Session, course_class=schemas.CourseClassCreate):
    new_course_class = models.CourseClass(**course_class.model_dump())
    db.add(new_course_class)
    db.flush()
    db.commit()
    return new_course_class

def delete_course_class(db: Session, class_id):
    db.delete(db.query(models.CourseClass).filter(models.CourseClass.id==class_id).first())
    db.flush()
    db.commit()

def get_all_attendance(db: Session):
    return db.query(models.Attendance).all()

def get_attendance_by_id(db:Session, id:str):
    return db.query(models.Attendance).filter(models.Attendance.id==id).first()

def get_attendance_by_student_id(db:Session, studentid: str):
    return db.query(models.Attendance).filter(models.Attendance.student_id==studentid).all()

def get_attendance_by_course_class_id(db: Session, courseclassid: str):
    return db.query(models.Attendance).filter(models.Attendance.course_class_id==courseclassid).all()

def create_attendance(db: Session, attendance: schemas.AttendanceCreate):
    new_attendance =  models.Attendance(student_id = attendance.student_id, course_class_id = attendance.course_class_id, present = False)
    db.add(new_attendance)
    db.flush()
    db.commit()
    return new_attendance

def update_attendance(db: Session, attendanceid: str, present:bool):
    attendance_to_update = db.query(models.Attendance).filter(models.Attendance.id==attendanceid).first()
    attendance_to_update.present = present
    db.flush()
    db.commit()
    return attendance_to_update

def delete_attendance(db: Session, attendanceid: str):
    db.delete(db.query(models.Attendance).filter_by(models.Attendance.id==attendanceid).first())
    db.flush()
    db.commit()