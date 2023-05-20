from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from starlette import status

from ..database import get_db
from ..models import BlogModel
from ..oauth2 import get_current_user
from ..schemas import BlogResponse, Blog, User

router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)


@router.post("/",
             response_model=BlogResponse,
             status_code=status.HTTP_201_CREATED)
def create(request: Blog, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_blog = BlogModel(**request.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.get("/",
            response_model=List[BlogResponse])
def create(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blogs = db.query(BlogModel).all()

    return blogs


@router.get("/{id}",
            response_model=Blog)
def create(id: int, response: Response, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {id} is not available."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available.")

    return blog


@router.delete("/{id}",
               status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = db.query(BlogModel).filter(BlogModel.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="blog with id {id} not found!")
    blog.delete(synchronize_session=False)
    db.commit()
    return None


@router.put("/blog/{id}",
            status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: Blog, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = db.query(BlogModel).filter(BlogModel.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="blog with id {id} not found!")
    blog.update(request.dict())
    db.commit()
    return "updated successfully"
