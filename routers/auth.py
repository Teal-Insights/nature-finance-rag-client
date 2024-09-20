from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response, Form
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import Session, select
from models import User
from utils import get_session, get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    organization_id: Optional[int] = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    organization_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    deleted: bool


@router.post("/register", response_class=RedirectResponse)
async def register(
    name: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
) -> RedirectResponse:
    user = UserCreate(name=name, email=email, password=password)
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Create access token
    access_token = create_access_token(data={"sub": db_user.email})

    # Set cookie
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="token", value=access_token, httponly=True)

    return response


@router.post("/login", response_class=RedirectResponse)
def login(
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
) -> RedirectResponse:
    db_user = session.exec(select(User).where(User.email == email)).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create access token
    access_token = create_access_token(data={"sub": db_user.email})

    # Set cookie
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="token", value=access_token, httponly=True)

    return response


@router.post("/forgot_password")
def forgot_password(user: UserCreate, session: Session = Depends(get_session)):
    # db_user = session.exec(select(User).where(
    #     User.email == user.email)).first()
    # TODO: Send reset password email
    return {
        "msg": "If an account with that email exists, a password reset link has been sent."
    }


@router.post("/reset_password")
def reset_password(
    token: str, new_password: str, session: Session = Depends(get_session)
):
    # TODO: Reset password
    return {"msg": "Password reset successfully"}


@router.get("/logout", response_class=RedirectResponse)
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("token")
    return response
