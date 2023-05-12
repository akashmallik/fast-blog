from fastapi import FastAPI

from .database import Base, engine
from .routers import blog, user

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)



