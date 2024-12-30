from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from app.schemas import ParentCreate
from app.utils.db import get_collection

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("")  # => /parent/ final
async def create_parent(parent: ParentCreate):
    parents = get_collection("parents")
    hashed_password = pwd_context.hash(parent.password)
    parent_data = parent.dict()
    parent_data["password"] = hashed_password

    result = await parents.insert_one(parent_data)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Could not create parent")
    return {"id": str(result.inserted_id)}
