from uuid import UUID

from pydantic import BaseModel, EmailStr


# Входные данные для регистрации
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Входные данные для логина
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Ответ с данными пользователя
class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


# Токен JWT
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
