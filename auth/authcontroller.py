from fastapi import HTTPException
from sqlalchemy.orm import Session
from utils.helper import hash_password, verify_password, create_token
from institute.models import Admin, Student
from utils.mail import send_mail

def admin_register(db: Session, data):
    existing_admin = db.query(Admin).filter(Admin.email == data.email).first()
    if existing_admin:
        raise HTTPException(
            status_code=400,
            detail="Admin with this email already exists"
        )

    admin = Admin(email=data.email, password=hash_password(data.password))
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return {"message": "Admin registered successfully"}

def admin_login(db: Session, data):
    admin = db.query(Admin).filter(Admin.email == data.email).first()
    if not admin or not verify_password(data.password, admin.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"role": "admin", "id": admin.id})
    return {"token": token}

async def student_register(db: Session, data):
    existing_student = db.query(Student).filter(Student.email == data.email).first()
    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Student with this email already exists"
        )
    student = Student(
        email=data.email,
        password=hash_password(data.password),
        name=data.email.split("@")[0]
    )
    db.add(student)
    db.commit()

    # send email
    try:
      await send_mail([student.email])
    except Exception as e:
      print(e)

    return {"message": "Student register"}

def student_login(db: Session, data):
    student = db.query(Student).filter(Student.email == data.email).first()
    if not student or not verify_password(data.password, student.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"role": "student", "id": student.id})
    return {"token": token}
