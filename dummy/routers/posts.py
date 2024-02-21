from typing import List 
from .. import schemas
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from ..database import get_db
from .. import models 
from fastapi import APIRouter 
from .. import utils

router = APIRouter(prefix="/posts", 
                   tags=["Posts"])


@router.get("/", response_model=List[schemas.GetPosts])
def getposts(db: Session = Depends(get_db)):
    data = db.query(models.Post).all()
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts are available")
    return data

@router.get("/{id}", response_model=schemas.GetPost)
def getpost(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Post).filter(models.Post.id == id)
    if not data.first(): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with {id} is available")
    return data.first()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreatePostResponse)
def createpost(post: schemas.PostBase, db: Session = Depends(get_db), get_current_user: int = Depends(utils.getcurrent_user)):
    data = models.Post(**post.model_dump(), owner_id = get_current_user)
    db.add(data)
    db.commit() 
    db.refresh(data)
    return data

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletepost(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Post).filter(models.Post.id == id)
    if not data.first(): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with {id} is available to delete")
    db.delete(data.first())
    db.commit()

''' task 
only allow user to update content 
then return title & content
'''
@router.put("/{id}", response_model=schemas.UpdatePostResponse)
def updatepost(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db)): 
    data = db.query(models.Post).filter(models.Post.id == id)
    if not data.first(): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} not found to update")
    data.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return data 
