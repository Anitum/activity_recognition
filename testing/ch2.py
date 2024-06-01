from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    user_type = Column(String)

    courses_taught = relationship('Course', backref='teacher', lazy='dynamic')
    enrollments = relationship('Enrollment', backref='student', lazy='dynamic')
    attendances = relationship('Attendance', backref='student', lazy='dynamic')

    def __repr__(self):
        return f"<User(user_id='{self.user_id}', name='{self.name}', email='{self.email}', user_type='{self.user_type}')>"

class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True)
    course_name = Column(String)
    course_code = Column(String)
    teacher_id = Column(Integer, ForeignKey('users.user_id'))

    enrollments = relationship('Enrollment', backref='course', lazy='dynamic')
    lectures = relationship('Lecture', backref='course', lazy='dynamic')

    def __repr__(self):
        return f"<Course(course_id='{self.course_id}', course_name='{self.course_name}', course_code='{self.course_code}', teacher_id='{self.teacher_id}')>"

class Enrollment(Base):
    __tablename__ = 'enrollments'

    enrollment_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('users.user_id'))
    course_id = Column(Integer, ForeignKey('courses.course_id'))

    def __repr__(self):
        return f"<Enrollment(enrollment_id='{self.enrollment_id}', student_id='{self.student_id}', course_id='{self.course_id}')>"

class Lecture(Base):
    __tablename__ = 'lectures'

    lecture_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    lecture_datetime = Column(DateTime)
    lecture_location = Column(String)

    attendances = relationship('Attendance', backref='lecture', lazy='dynamic')

    def __repr__(self):
        return f"<Lecture(lecture_id='{self.lecture_id}', course_id='{self.course_id}', lecture_datetime='{self.lecture_datetime}', lecture_location='{self.lecture_location}')>"

class Attendance(Base):
    __tablename__ = 'attendances'

    attendance_id = Column(Integer, primary_key=True)
    lecture_id = Column(Integer, ForeignKey('lectures.lecture_id'))
    student_id = Column(Integer, ForeignKey('users.user_id'))
    attendance_status = Column(String)

    def __repr__(self):
        return f"<Attendance(attendance_id='{self.attendance_id}', lecture_id='{self.lecture_id}', student_id='{self.student_id}', attendance_status='{self.attendance_status}')>"