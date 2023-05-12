from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .. import hashing
from ..database import get_db
from ..models import UserModel
from ..schemas import User, UserResponse

router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=UserResponse)
def create_user(request: User, db: Session = Depends(get_db)):
    hashed_password = hashing.bcrypt(request.password)
    user_data = request.dict()
    user_data.update({"password": hashed_password})
    new_user = UserModel(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}",
            response_model=UserResponse)
def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available.")

    return user
