from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from pydantic import Field, BaseModel
from starlette import status

from models import Todos
from models import Users
from database import SessionLocal
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from .auth import get_current_user

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


class UserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    is_active: bool
    role: str


@router.get("/todos")
async def read_all(user: user_dependency,db: db_dependency):
    return db.query(Todos).all()


@router.get("/users")
async def read_all(db: db_dependency):
    return db.query(Users).all()


@router.get("/todo/{todo_id}")
async def getByID(user: user_dependency,
                  db: db_dependency, todo_id: int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='TODO not found. ')


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,
                      db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed.')
    todo_model = Todos(**todo_request.dict(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserRequest):
    user_model = Users(**user_request.dict())
    db.add(user_model)
    db.commit()
