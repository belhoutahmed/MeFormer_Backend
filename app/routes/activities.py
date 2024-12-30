from fastapi import APIRouter
from app.utils.db import get_collection

router = APIRouter()

@router.get("/{student_id}")
async def get_student_activities(student_id: str):
    activities = get_collection("activities")
    return await activities.find({"student_id": student_id}).to_list(length=100)
