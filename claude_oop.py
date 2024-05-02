import face_recognition
import cv2
import numpy as np
import datetime

class User:
    def __init__(self, name, user_type, image):
        self.name = name
        self.user_type = user_type  # "student" or "teacher"
        self.encoding = face_recognition.face_encodings(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))[0]

class Course:
    def __init__(self, name, code, teacher):
        self.name = name
        self.code = code
        self.teacher = teacher
        self.students = []

class Enrollment:
    def __init__(self, student, course):
        self.student = student
        self.course = course
        self.attendance = []

class Attendance:
    def __init__(self, student, course, date, status):
        self.student = student
        self.course = course
        self.date = date
        self.status = status  # "present", "absent", or "late"

class AttendanceSystem:
    def __init__(self):
        self.users = []
        self.courses = []
        self.enrollments = []

    def add_user(self, name, user_type, image):
        user = User(name, user_type, image)
        self.users.append(user)

    def add_course(self, name, code, teacher):
        course = Course(name, code, teacher)
        self.courses.append(course)

    def enroll_student(self, student, course):
        enrollment = Enrollment(student, course)
        self.enrollments.append(enrollment)
        course.students.append(student)

    def mark_attendance(self, image):
        encoding = face_recognition.face_encodings(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))[0]
        matches = face_recognition.compare_faces([user.encoding for user in self.users], encoding)
        student = next((user for user, match in zip(self.users, matches) if match), None)

        if student:
            date = datetime.datetime.now().date()
            for enrollment in self.enrollments:
                if enrollment.student == student:
                    attendance = Attendance(student, enrollment.course, date, "present")
                    enrollment.attendance.append(attendance)
                    print(f"{student.name} is present for {enrollment.course.name}")
        else:
            print("Unknown person")

