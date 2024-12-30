from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas import ExerciseCreate, ExerciseResponse
from app.utils.db import get_collection
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=ExerciseResponse)
async def create_exercise(exercise: ExerciseCreate):
    exercises = get_collection("exercises")
    exercise_data = exercise.dict()
    result = await exercises.insert_one(exercise_data)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Could not create exercise")
    exercise_data["id"] = str(result.inserted_id)
    return exercise_data

@router.get("/", response_model=List[ExerciseResponse])
async def get_exercises():
    exercises = get_collection("exercises")
    exercise_list = await exercises.find().to_list(length=100)
    for exercise in exercise_list:
        exercise["id"] = str(exercise["_id"])
        del exercise["_id"]
    return exercise_list

@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise_by_id(exercise_id: str):
    exercises = get_collection("exercises")
    exercise = await exercises.find_one({"_id": ObjectId(exercise_id)})
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    exercise["id"] = str(exercise["_id"])
    del exercise["_id"]
    return exercise
