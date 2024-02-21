from typing import List 
from .. import schemas
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from ..database import get_db
from .. import models 
from .. import utils
from fastapi import APIRouter 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users", 
                   tags=["Users"]) 

@router.get("/", response_model=List[schemas.CreateUserResponse]) #
def getusers(db: Session = Depends(get_db), user_credential: int = Depends(utils.getcurrent_user)):
    data = db.query(models.User).all() 
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NO users are found")
    return data

@router.post("/", response_model=schemas.CreateUserResponse, status_code=status.HTTP_201_CREATED)
def createuser(user: schemas.CreateUser, db: Session = Depends(get_db)): 
    hashed_password = utils.createhashedpass(user.password)
    user.password = hashed_password 
    data = models.User(**user.model_dump())
    if not data: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.post("/login", response_model=schemas.LoginUserResponse)
def login(usercreds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): 
    data = db.query(models.User).filter(models.User.email == usercreds.username).first()
    if not data: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credetials")
    
    if not utils.verifypassword(usercreds.password, data.password): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credetials")
    return {"access_token": utils.createtoken({"id": data.id}),"token_type": "bearer"}