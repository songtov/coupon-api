from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.auth import authenticate_user, create_access_token, get_password_hash
from app.models.user import UserCreate, User, UserLogin, Token
from app.config import settings
from app.db import get_db

router = APIRouter()

@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db = Depends(get_db)):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data.pop("password")
    user_data["hashed_password"] = hashed_password
    
    result = await db.users.insert_one(user_data)
    created_user = await db.users.find_one({"_id": result.inserted_id})
    
    return User(id=str(created_user["_id"]), **{k: v for k, v in created_user.items() if k != "_id"})

@router.post("/login", response_model=Token)
async def login_user(user_login: UserLogin, db = Depends(get_db)):
    user = await authenticate_user(user_login.email, user_login.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    # OAuth2PasswordRequestForm uses 'username' field, but we treat it as email
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}