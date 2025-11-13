from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from utils.password import hash_password, verify_password
from utils.jwt_handler import create_access_token
from schemas.user import RegisterRequest, LoginRequest

def register_user(data: RegisterRequest, db: Session):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(username=data.username, email=data.email, password=hash_password(data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(data: LoginRequest, db: Session):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}