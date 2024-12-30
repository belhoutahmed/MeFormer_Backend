from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta


from app.config import settings
from app.utils.db import get_collection

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=None)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Route pour l'authentification d'un parent.
    `form_data` est injecté avec Depends(OAuth2PasswordRequestForm).
    """
    parents_collection = get_collection("parents")
    
    # On recherche le document parent via l'email (qui correspond à form_data.username)
    parent = await parents_collection.find_one({"email": form_data.username})
    
    # Vérification de l'existence du parent et du mot de passe
    if not parent or not pwd_context.verify(form_data.password, parent["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Création du payload pour le token JWT
    token_data = {
        "sub": str(parent["_id"]),
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    # Encodage du token avec la clé secrète et l'algorithme défini
    token = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    # Renvoyer le token
    return {"access_token": token, "token_type": "bearer"}
