from typing import List
from fastapi import FastAPI, status, Depends, HTTPException
from .database import *
from sqlalchemy.orm import Session
from . import models
from .schemas import * 
from .routers import posts, users
models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

@app.get("/")
def greetings(): 
    return "welcome to fastapi"

app.include_router(posts.router)
app.include_router(users.router)
   
    