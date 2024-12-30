from bson import ObjectId
from app.utils.db import get_collection
from fastapi import APIRouter, HTTPException


router = APIRouter()

def serialize_article(article):
    # Convert ObjectId to string for JSON serialization
    if "_id" in article:
        article["_id"] = str(article["_id"])
    return article

@router.get("/")
async def get_all_articles():
    articles = get_collection("articles")
    articles_list = await articles.find().to_list(length=100)
    # Serialize each article
    return [serialize_article(article) for article in articles_list]

@router.get("/{article_id}")
async def get_article(article_id: str):
    articles = get_collection("articles")
    article = await articles.find_one({"_id": ObjectId(article_id)})
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    # Serialize the article
    return serialize_article(article)
