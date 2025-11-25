from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.security import decode_access_token
from backend.app.db.session import get_db
from backend.app.schemas.user import Token, UserCreate, UserRead
from backend.app.services.user_service import AuthService

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/register", response_model=UserRead)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await AuthService.register(data, db)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    token = await AuthService.authenticate(form_data.username, form_data.password, db)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def read_users_me(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    user_id = decode_access_token(token)
    user = await AuthService.get_current_user(user_id, db)
    return user
