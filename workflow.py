from claude_oop import db, User, Student, Parent, Teacher, Course, Enrollment, Lecture, Attendance, Notification
from ch1 import send_notification
from ch2 import db, User, Course, Enrollment, Lecture, Attendance, Notification


lecture = Lecture(
    course_id=course.course_id,
    lecture_datetime=datetime.datetime(2023, 5, 15, 10, 0),
    lecture_location='Room 101'
)
db.session.add(lecture)
db.session.commit()

# 2. Capturing attendance during the lecture
for enrollment in course.enrollments:
    attendance = Attendance(
        lecture_id=lecture.lecture_id,
        student_id=enrollment.student_id,
        attendance_status='present'  # or 'absent' or 'late'
    )
    db.session.add(attendance)
db.session.commit()

# 3. Generating notifications after attendance is recorded
for enrollment in course.enrollments:
    student = enrollment.student
    teacher = course.teacher

    # Notification for student
    notification = Notification(
        notification_message=f'Attendance marked for {course.course_name} on {lecture.lecture_datetime}',
        recipient_id=student.user_id,
        notification_type='Attendance'
    )
    db.session.add(notification)

    # Notification for teacher
    notification = Notification(
        notification_message=f'Attendance recorded for {course.course_name} on {lecture.lecture_datetime}',
        recipient_id=teacher.user_id,
        notification_type='Attendance'
    )
    db.session.add(notification)

    # Notification for parent (if applicable)
    if student.parent:
        notification = Notification(
            notification_message=f'{student.name} was {"present" if attendance.attendance_status == "present" else "absent"} for {course.course_name} on {lecture.lecture_datetime}',
            recipient_id=student.parent.user_id,
            notification_type='Attendance'
        )
        db.session.add(notification)

db.session.commit()

# 4. Sending notifications (via email, SMS, or other channels)
for notification in Notification.query.all():
    send_notification(notification)

# 5. Data stored in the respective tables