from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate


class AuthService:
    @staticmethod
    async def register(data: UserCreate, db: AsyncSession) -> User:
        # check email
        result = await db.execute(select(User).filter(User.email == data.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        # check username
        result = await db.execute(select(User).filter(User.username == data.username))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists",
            )

        # Создание пользователя
        user = User(
            email=data.email,
            username=data.username,
            hashed_password=get_password_hash(data.password),
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def authenticate(email: str, password: str, db: AsyncSession) -> str:
        result = await db.execute(select(User).filter(User.email == email))
        user = result.scalars().first()

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            subject=str(user.id), expires_delta=access_token_expires
        )

    @staticmethod
    async def get_current_user(user_id: str, db: AsyncSession) -> User:
        from sqlalchemy import select

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
