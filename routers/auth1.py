from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Annotated
from models import Users
from fastapi.security import OAuth2PasswordRequestForm
from database import SessionLocal
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from routers.todos import bcrypt_context

router = APIRouter()

# security.py
from passlib.context import CryptContext


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


# Accept bcrypt; add others ONLY if you actually stored those historically
pwd_context = CryptContext(
    schemes=["bcrypt"],  # or ["bcrypt", "pbkdf2_sha256", "argon2"] if you truly have mixed hashes
    deprecated="auto",
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


@router.post('/auth')
async def create_user(create_user_request: CreateUserRequest):
    return {'user': 'authenticated.'}


@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return " Failed Authentication."
    return " Successful Authentication."
