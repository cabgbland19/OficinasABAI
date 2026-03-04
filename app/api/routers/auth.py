from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_db, get_current_user, require_roles
from app.core.config import settings
from app.core.security import verify_password, create_access_token, get_password_hash
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.username == form.username)).scalar_one_or_none()
    if user is None or not verify_password(form.password, user.hashed_password) or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token = create_access_token(
        subject=user.username,
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        expires_minutes=settings.access_token_expire_minutes,
        extra={"role": user.role},
    )
    return Token(access_token=token)

@router.get("/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)):
    return UserRead(id=user.id, username=user.username, role=user.role, is_active=user.is_active)

@router.post("/users", response_model=UserRead, status_code=201, dependencies=[Depends(require_roles("admin"))])
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if payload.role not in {"admin", "writer", "reader"}:
        raise HTTPException(status_code=400, detail="Invalid role")

    exists = db.execute(select(User).where(User.username == payload.username)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Username already exists")

    user = User(
        username=payload.username,
        hashed_password=get_password_hash(payload.password),
        role=payload.role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead(id=user.id, username=user.username, role=user.role, is_active=user.is_active)