from pydantic import BaseModel, EmailStr
from typing import List, Optional

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class StudentLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ExerciseBase(BaseModel):
    question: str
    type: str  # "qcm" or "open-ended"
    options: Optional[List[str]] = None  # Only for QCM
    correct_answer: Optional[str] = None  # Only for QCM

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseResponse(ExerciseBase):
    id: str