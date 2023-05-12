from typing import List

from fastapi import FastAPI, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from . import hashing
from .database import Base, engine, SessionLocal
from .models import BlogModel, UserModel
from .schemas import Blog, User, UserResponse, BlogResponse

app = FastAPI()

Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", response_model=BlogResponse, status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = BlogModel(**request.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.get("/blog", response_model=List[BlogResponse], tags=["blogs"])
def create(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()

    return blogs


@app.get("/blog/{id}", response_model=Blog, tags=["blogs"])
def create(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {id} is not available."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available.")

    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="blog with id {id} not found!")
    blog.delete(synchronize_session=False)
    db.commit()
    return None


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id: int, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="blog with id {id} not found!")
    blog.update(request.dict())
    db.commit()
    return "updated successfully"


@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=UserResponse, tags=["users"])
def create_user(request: User, db: Session = Depends(get_db)):
    hashed_password = hashing.bcrypt(request.password)
    user_data = request.dict()
    user_data.update({"password": hashed_password})
    new_user = UserModel(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/user/{id}", response_model=UserResponse, tags=["users"])
def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available.")

    return user
