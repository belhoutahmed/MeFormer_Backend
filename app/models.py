from pydantic import BaseModel, EmailStr

class StudentModel(BaseModel):
    name: str
    email: EmailStr
    password: str
    progress: dict = {}

class ArticleModel(BaseModel):
    title: str
    content: str
    category: str  # video, fiche, présentation
    created_at: str

class ActivityModel(BaseModel):
    student_id: str
    action: str
    timestamp: str

class Article(BaseModel):
    title: str
    category: str
    content: str
    created_at: str
