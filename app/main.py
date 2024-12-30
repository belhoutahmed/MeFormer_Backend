from fastapi import FastAPI
from app.routes import student, articles, activities,exercises

app = FastAPI()

# Inclure les routes
app.include_router(student.router, prefix="/student", tags=["Student"])
app.include_router(articles.router, prefix="/articles", tags=["Articles"])
app.include_router(activities.router, prefix="/activities", tags=["Activities"])
app.include_router(exercises.router, prefix="/exercises", tags=["Exercises"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Education Backend"}
