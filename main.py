from fastapi import FastAPI
from utils.db import Base, engine
from auth.authrouter import router as auth_router
from institute.router import router as institute_router
from attendance.attendance_router import router as attendance_router

def create_table():
    Base.metadata.create_all(bind=engine)
create_table()

app = FastAPI(title="Institute Management System")

app.include_router(auth_router)
app.include_router(institute_router)
app.include_router(attendance_router)

