from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, CheckConstraint, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True)
    password = Column(String(255), nullable=False)
    role = Column(String(30), CheckConstraint("role in ('admin', 'instructor', 'student')"), nullable=False)
    name = Column(String(255), nullable=False)

    instructor = relationship("Instructor", back_populates="user", cascade="all, delete", passive_deletes=True)
    student = relationship("Student", back_populates="user", cascade="all, delete", passive_deletes=True)

class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=True)
    

    user = relationship("User", back_populates="instructor")
    courses = relationship("Course", back_populates="instructor", cascade="all, delete", passive_deletes=True)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=True)

    user = relationship("User", back_populates="student")
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete", passive_deletes=True)
    attendance = relationship("Attendance", back_populates="student", cascade="all, delete", passive_deletes=True)


class Course(Base):
    __tablename__ = "courses"

    instructor_id = Column(String(255), ForeignKey("instructors.user_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    code = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)

    instructor = relationship("Instructor", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete", passive_deletes=True)
    course_classes = relationship("CourseClass", back_populates="course", cascade="all, delete", passive_deletes=True)

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(255), ForeignKey("students.user_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    course_code = Column(String(255), ForeignKey("courses.code", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class CourseClass(Base):
    __tablename__ = "course_classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_time = Column(DateTime)
    course_code = Column(String(255), ForeignKey("courses.code", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    course = relationship("Course", back_populates="course_classes")
    attendance = relationship("Attendance", back_populates="course_class", cascade="all, delete", passive_deletes=True)



class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(255), ForeignKey("students.user_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    course_class_id = Column(Integer, ForeignKey("course_classes.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    present = Column(Boolean, nullable=False)

    student = relationship("Student", back_populates="attendance")
    course_class = relationship("CourseClass", back_populates="attendance")

# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True)
#     title = Column(String(255), index=True)
#     description = Column(String(255), index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")