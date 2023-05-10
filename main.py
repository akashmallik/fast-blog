from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/blog")
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    # only get 10 published blog
    if published:
        return {"data": f"{limit} published blogs from the db"}

    return {"data": f"{limit} blogs from the db"}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post("/blog")
def create_blog(blog: Blog):
    return {"data": f"Blog is created with {blog.title}"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}


@app.get("/blog/{id}")
def show(id: int):
    # fetch blog with id = id
    return {"data": id}


@app.get("/blog/{id}/comments")
def comments(id: int):
    # fetch comments of blog with id = id
    return {"data": {"comment 01", "comment 02"}}
