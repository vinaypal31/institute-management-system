from sqlalchemy.orm import Session
from sqlalchemy import func
from institute.models import Teacher, Course, Enrollment, Fees, Student, TeacherCourse, Attendance
from fastapi import HTTPException

# -------------------- TEACHER --------------------

def add_teacher(db: Session, name: str):
    teacher = Teacher(name=name)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return {"message": "Teacher added", "teacher_id": teacher.id}


def upsert_teacher(body, db: Session):
    if body.teacher_id:
        teacher = db.query(Teacher).filter(Teacher.id == body.teacher_id).first()
        if not teacher:
            return {"error": "Teacher not found"}

        teacher.name = body.name
        db.commit()
        db.refresh(teacher)
        return {"message": "Teacher updated", "teacher_id": teacher.id}

    teacher = Teacher(name=body.name)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return {"message": "Teacher created", "teacher_id": teacher.id}


def delete_teacher(db: Session, teacher_id: int):
    # remove mappings first
    db.query(TeacherCourse).filter(TeacherCourse.teacher_id == teacher_id).delete()
    db.query(Teacher).filter(Teacher.id == teacher_id).delete()
    db.commit()
    return {"message": "Teacher deleted"}


# -------------------- COURSE --------------------

def add_course(db: Session, name: str):
    course = Course(name=name)
    db.add(course)
    db.commit()
    db.refresh(course)
    return {"message": "Course added", "course_id": course.id}


def update_course(db: Session, course_id: int, name: str):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        return {"error": "Course not found"}

    course.name = name
    db.commit()
    return {"message": "Course updated"}


def delete_course(db: Session, course_id: int):
    db.query(Enrollment).filter(Enrollment.course_id == course_id).delete()

    db.query(TeacherCourse).filter(TeacherCourse.course_id == course_id).delete()

    db.query(Course).filter(Course.id == course_id).delete()

    db.commit()
    return {"message": "Course deleted"}


# -------------------- ASSIGN / UNASSIGN --------------------

def assign_teacher_to_course(db: Session, teacher_id: int, course_id: int):
    tc = TeacherCourse(teacher_id=teacher_id,course_id=course_id)
    db.add(tc)
    db.commit()
    return {"message": "Teacher assigned to course"}


def unassign_teacher_from_course(db: Session, teacher_id: int, course_id: int):
    db.query(TeacherCourse).filter(TeacherCourse.teacher_id == teacher_id,TeacherCourse.course_id == course_id).delete()

    db.commit()
    return {"message": "Teacher unassigned from course"}


# -------------------- STUDENT --------------------

def enroll_student(db: Session, student_id: int, course_id: int):
    sd = Enrollment(student_id=student_id,course_id=course_id)
    db.add(sd)
    db.commit()
    return {"message": "Student enrolled to course"}


def unenroll_student(db: Session, student_id: int, course_id: int):
    db.query(Enrollment).filter(Enrollment.student_id == student_id,Enrollment.course_id == course_id).delete()

    db.commit()
    return {"message": "Student unenrolled from course"}


def delete_student(db: Session, student_id: int):
    db.query(Enrollment).filter(Enrollment.student_id == student_id).delete()

    db.query(Fees).filter(Fees.student_id == student_id).delete()

    db.query(Student).filter(Student.id == student_id).delete()

    db.commit()
    return {"message": "Student deleted"}


# -------------------- FEES --------------------

def setup_fees(db: Session, student_id: int, total: int):
    fees = Fees(student_id=student_id, total=total)
    db.add(fees)
    db.commit()
    return {"message": "Fees setup"}


def pay_fees(db: Session, student_id: int, amount: int):
    fees = db.query(Fees).filter(Fees.student_id == student_id).first()
    if not fees:
        return {"error": "Fees not found"}

    fees.paid += amount
    db.commit()
    return {"message": "Fees paid"}


# -------------------- STUDENT VIEW --------------------

def get_student_profile(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    return {
        "id": student.id,
        "name": student.name,
        "email": student.email
    }


def get_my_course(db: Session, student_id: int):
    mapping = db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).first()

    course = db.query(Course).filter(
        Course.id == mapping.course_id
    ).first()

    return {"course_id": course.id, "course_name": course.name}


def get_my_fees(db: Session, student_id: int):
    fees = db.query(Fees).filter(Fees.student_id == student_id).first()
    return {
        "total": fees.total,
        "paid": fees.paid,
        "pending": fees.total - fees.paid
    }


# -------------------- COUNTS & SUMMARY --------------------

def get_all_course_student_count(db: Session):
    result = (
        db.query(
            Course.id,
            Course.name,
            func.count(Enrollment.student_id).label("total_students")
        )
        .outerjoin(Enrollment, Course.id == Enrollment.course_id)
        .group_by(Course.id)
        .all()
    )

    return [
        {
            "course_id": row.id,
            "course_name": row.name,
            "total_students": row.total_students
        }
        for row in result
    ]


def get_single_course_student_count(course_id: int, db: Session):
    count = db.query(func.count(Enrollment.student_id))\
              .filter(Enrollment.course_id == course_id)\
              .scalar()
    return {"course_id": course_id, "total_students": count}


def get_course_teacher_count(course_id: int, db: Session):
    count = db.query(func.count(TeacherCourse.teacher_id))\
              .filter(TeacherCourse.course_id == course_id)\
              .scalar()
    return {"course_id": course_id, "total_teachers": count}


def get_course_summary(course_id: int, db: Session):
    return {
        "course_id": course_id,
        "total_students": db.query(func.count(Enrollment.student_id)).filter(Enrollment.course_id == course_id).scalar(),
        "total_teachers": db.query(func.count(TeacherCourse.teacher_id)).filter(TeacherCourse.course_id == course_id).scalar()
    }

