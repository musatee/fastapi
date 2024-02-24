from typing import List
from fastapi import FastAPI, status, Depends, HTTPException
from .database import *
from sqlalchemy.orm import Session
from . import models
from .schemas import * 
from .routers import posts, users, votes 
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def greetings(): 
    return "welcome to fastapi"

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)
   
    