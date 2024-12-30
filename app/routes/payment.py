from fastapi import APIRouter, HTTPException
from app.utils.db import get_collection

router = APIRouter()

@router.post("/{parent_id}")
async def create_payment(parent_id: str, payment_details: dict):
    parents = get_collection("parents")
    result = await parents.update_one(
        {"_id": parent_id},
        {"$set": {"payment_info": payment_details}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Parent not found or no changes made")
    return {"message": "Payment details updated successfully"}
