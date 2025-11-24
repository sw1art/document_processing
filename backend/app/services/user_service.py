from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.security import get_password_hash, verify_password
from backend.app.models.user import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, email: str, password: str) -> User:
        hashed_password = get_password_hash(password)
        user = User(email=email, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authenticate_user(self, email: str, password: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user and verify_password(password, user.hashed_password):
            return user
        return None
