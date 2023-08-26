from fastapi import FastAPI
from . import models
from .db import engine
from .routers import users, auth

# migration used alembic
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def hello():
    return {"message": "hello world"}
