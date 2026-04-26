from sqlalchemy.orm import Session
from institute.models import Attendance

def mark_attendance(db: Session, data):
    attendance = Attendance(
        student_id=data.student_id,
        course_id=data.course_id,
        date=data.date,
        status=data.status
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return {"message": "Attendance marked"}

def get_attendance_by_student(db: Session, student_id: int):
    records = db.query(Attendance).filter(Attendance.student_id == student_id).all()
    return records