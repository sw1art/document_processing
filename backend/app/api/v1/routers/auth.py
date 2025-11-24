from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.v1.deps import get_current_user
from backend.app.core.security import create_access_token
from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.schemas.user import Token, UserCreate, UserLogin, UserRead
from backend.app.services.user_service import UserService

router = APIRouter()


# Эндпоинт регистрации
@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    # Проверяем, есть ли уже пользователь
    existing_user = await service.authenticate_user(user_in.email, user_in.password)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    user = await service.create_user(user_in.email, user_in.password)
    return user


# Эндпоинт логина
@router.post("/login", response_model=Token)
async def login(form_data: UserLogin, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)


# Защищенный эндпоинт для получения пользователя
@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
