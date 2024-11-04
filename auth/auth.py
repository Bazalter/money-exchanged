from datetime import timedelta
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from sql_app.database import SessionLocal
from .crud import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user
from .crud import get_current_active_user
from .schemas import Token, UserInDB


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


dp_dependency = Annotated[Session, Depends(get_db)]


@router.post("/token", response_model=None)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: dp_dependency
                                 ) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# # Закрытый маршрут, доступен только авторизованным пользователям


@router.get("/private")
async def read_private(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    return {"message": f"Hello, {current_user.username}. This is a private route, only for authorized users."}


@router.get("/users/me/", response_model=UserInDB)
async def read_users_me(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    return current_user
