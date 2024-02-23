from typing import List 
from .. import schemas
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from ..database import get_db
from .. import models 
from fastapi import APIRouter 
from .. import utils

router = APIRouter(prefix="/votes", 
                   tags=["Votings"]) 

@router.post("/", status_code=status.HTTP_201_CREATED)
def createvote(vote: schemas.Vote, db: Session = Depends(get_db), get_current_user: int = Depends(utils.getcurrent_user)):
    data = models.Vote(**vote.model_dump(), user_id = get_current_user)
    db.add(data)
    db.commit() 
    db.refresh(data)
    return data