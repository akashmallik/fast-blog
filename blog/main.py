from fastapi import FastAPI, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .database import Base, engine, SessionLocal
from .models import BlogModel
from .schemas import Blog

app = FastAPI()

Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(blog: Blog, db: Session = Depends(get_db)):
    new_blog = BlogModel(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.get("/blog")
def create(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()

    return blogs


@app.get("/blog/{id}")
def create(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {id} is not available."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available.")

    return blog
