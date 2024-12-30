from fastapi import APIRouter, HTTPException
from app.schemas import CourseCreate
from app.utils.db import get_collection

router = APIRouter()

@router.post("/")
async def create_course(course: CourseCreate):
    courses = get_collection("courses")
    course_data = course.dict()
    result = await courses.insert_one(course_data)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Could not create course")
    return {"id": str(result.inserted_id)}

@router.get("/")
async def get_all_courses():
    courses = get_collection("courses")
    course_list = await courses.find().to_list(100)
    return course_list
