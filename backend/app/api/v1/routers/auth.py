from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.v1.deps import get_current_user
from backend.app.db.session import get_db
from backend.app.schemas.user import Token, UserCreate, UserLogin, UserRead
from backend.app.services.user_service import AuthService

router = APIRouter()


# Эндпоинт регистрации
@router.post("/register", response_model=UserRead)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await AuthService.register(data, db)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Эндпоинт логина
@router.post("/login", response_model=Token)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        token = await AuthService.authenticate(data, db)
        return Token(access_token=token)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid credentials")


# Защищенный эндпоинт для получения пользователя
@router.get("/me", response_model=UserRead)
async def me(current_user=Depends(get_current_user)):
    return current_user
