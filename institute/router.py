from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.db import get_db
from institute import controller
from utils.helper import admin_required, student_required
from auth.dtos import TeacherUpsert

router = APIRouter(prefix="/institute")

# -------------------- TEACHER -------------------

@router.post("/teacher", dependencies=[Depends(admin_required)])
def add_teacher(name: str, db: Session = Depends(get_db)):
    return controller.add_teacher(db, name)

@router.post("/teacher/upsert", dependencies=[Depends(admin_required)])
def upsert_teacher(body: TeacherUpsert, db: Session = Depends(get_db)):
    return controller.upsert_teacher(body, db)

@router.delete("/teacher/{teacher_id}", dependencies=[Depends(admin_required)])
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    return controller.delete_teacher(db, teacher_id)

# -------------------- COURSE -------------------

@router.post("/course", dependencies=[Depends(admin_required)])
def add_course(name: str, db: Session = Depends(get_db)):
    return controller.add_course(db, name)

@router.put("/course/{course_id}", dependencies=[Depends(admin_required)])
def update_course(course_id: int, name: str, db: Session = Depends(get_db)):
    return controller.update_course(db, course_id, name)

@router.delete("/course/{course_id}", dependencies=[Depends(admin_required)])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    return controller.delete_course(db, course_id)

# -------------------- ASSIGN / UNASSIGN --------------------

@router.post("/assign-teacher", dependencies=[Depends(admin_required)])
def assign_teacher(teacher_id: int, course_id: int, db: Session = Depends(get_db)):
    return controller.assign_teacher_to_course(db, teacher_id, course_id)

@router.delete("/unassign-teacher", dependencies=[Depends(admin_required)])
def unassign_teacher(teacher_id: int, course_id: int, db: Session = Depends(get_db)):
    return controller.unassign_teacher_from_course(db, teacher_id, course_id)

# -------------------- STUDENT --------------------

@router.post("/enroll", dependencies=[Depends(admin_required)])
def enroll(student_id: int, course_id: int, db: Session = Depends(get_db)):
    return controller.enroll_student(db, student_id, course_id)

@router.delete("/unenroll", dependencies=[Depends(admin_required)])
def unenroll(student_id: int, course_id: int, db: Session = Depends(get_db)):
    return controller.unenroll_student(db, student_id, course_id)

@router.delete("/student/{student_id}", dependencies=[Depends(admin_required)])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return controller.delete_student(db, student_id)

# -------------------- FEES --------------------

@router.post("/fees", dependencies=[Depends(admin_required)])
def setup_fees(student_id: int, total: int, db: Session = Depends(get_db)):
    return controller.setup_fees(db, student_id, total)

@router.post("/pay", dependencies=[Depends(student_required)])
def pay_fees(student_id: int, amount: int, db: Session = Depends(get_db)):
    return controller.pay_fees(db, student_id, amount)

# -------------------- STUDENT VIEW --------------------

@router.get("/student/profile", dependencies=[Depends(student_required)])
def student_profile(user=Depends(student_required), db: Session = Depends(get_db)):
    return controller.get_student_profile(db, user["id"])

@router.get("/student/my-course", dependencies=[Depends(student_required)])
def my_course(user=Depends(student_required), db: Session = Depends(get_db)):
    return controller.get_my_course(db, user["id"])

@router.get("/student/fees", dependencies=[Depends(student_required)])
def student_fees(user=Depends(student_required), db: Session = Depends(get_db)):
    return controller.get_my_fees(db, user["id"])

# -------------------- COUNTS & SUMMARY --------------------

@router.get("/student/count", dependencies=[Depends(admin_required)])
def all_course_student_count(db: Session = Depends(get_db)):
    return controller.get_all_course_student_count(db)

@router.get("/{course_id}/student/count", dependencies=[Depends(admin_required)])
def single_course_student_count(course_id: int, db: Session = Depends(get_db)):
    return controller.get_single_course_student_count(course_id, db)

@router.get("/{course_id}/teacher/count", dependencies=[Depends(admin_required)])
def course_teacher_count(course_id: int, db: Session = Depends(get_db)):
    return controller.get_course_teacher_count(course_id, db)

@router.get("/{course_id}/summary", dependencies=[Depends(admin_required)])
def course_summary(course_id: int, db: Session = Depends(get_db)):
    return controller.get_course_summary(course_id, db)
