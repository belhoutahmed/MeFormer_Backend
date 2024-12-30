from fastapi import APIRouter, HTTPException
from app.schemas import StudentCreate, StudentLogin, TokenResponse
from app.utils.db import get_collection
from app.utils.auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register")
async def register_student(student: StudentCreate):
    students = get_collection("students")
    existing_student = await students.find_one({"email": student.email})
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    student_data = student.dict()
    student_data["password"] = hash_password(student.password)
    await students.insert_one(student_data)
    return {"message": "Student registered successfully"}

@router.post("/login", response_model=TokenResponse)
async def login_student(student: StudentLogin):
    print(f"Received email: {student.email}")
    students = get_collection("students")
    student_data = await students.find_one({"email": student.email})
    if not student_data:
        print("No student found with this email")
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(student.password, student_data["password"]):
        print("Password verification failed")
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    print("Login successful")
    token = create_access_token(data={"sub": str(student_data["_id"])})
    return {"access_token": token, "token_type": "bearer"}

