from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.db import get_db
from auth import dtos
from attendance import attendance_controller

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/mark")
def mark_attendance(data: dtos.AttendanceCreate, db: Session = Depends(get_db)):
    return attendance_controller.mark_attendance(db, data)

@router.get("/student/{student_id}")
def get_attendance(student_id: int, db: Session = Depends(get_db)):
    return attendance_controller.get_attendance_by_student(db, student_id)