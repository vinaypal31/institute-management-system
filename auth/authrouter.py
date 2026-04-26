from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.db import get_db
from auth import authcontroller, dtos

router = APIRouter(prefix="/auth")

@router.post("/admin/register")
def admin_register(body: dtos.Register, db: Session = Depends(get_db)):
    return authcontroller.admin_register(db, body)

@router.post("/admin/login")
def admin_login(body: dtos.Login, db: Session = Depends(get_db)):
    return authcontroller.admin_login(db, body)

@router.post("/student/register")
async def student_register(body: dtos.Register, db: Session = Depends(get_db)):
    return await authcontroller.student_register(db, body)

@router.post("/student/login")
def student_login(body: dtos.Login, db: Session = Depends(get_db)):
    return authcontroller.student_login(db, body)
