from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.user import RegisterRequest, LoginRequest, UserResponse, TokenResponse
from services.auth_service import register_user, login_user
from database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(data, db)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(data, db)