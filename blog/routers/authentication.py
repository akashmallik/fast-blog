from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..database import get_db
from ..hashing import verify
from ..models import UserModel
from ..schemas import Login
from ..token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter()


@router.post("/login")
def login(request: Login, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(
        UserModel.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")

    if not verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
