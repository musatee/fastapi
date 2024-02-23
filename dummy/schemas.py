from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel): 
    title: str 
    content: str 
    published: bool = True 

class GetPosts(PostBase): 
    id: int
    class Config:
        orm_mode = True
        
class GetPost(PostBase): 
    class Config:
        orm_mode = True 

class CreateUser(BaseModel): 
    email: EmailStr
    password: str 

class CreateUserResponse(BaseModel): 
    id: int
    email: EmailStr
    class Config: 
        orm_mode = True 

class CreatePostResponse(BaseModel):
    title: str 
    content: str 
    created_at: datetime 
    class Config:
        orm_mode = True 
    owner: CreateUserResponse

class DeletePost(BaseModel): 
    title: str
    content: str 

class UpdatePost(BaseModel): 
    content: str

class UpdatePostResponse(BaseModel): 
    title: str 
    content: str 
    class Config: 
        orm_mode = True 

class LoginUserResponse(BaseModel): 
    access_token: str
    token_type: str 
    class Config: 
        orm_mode = True 

class TokenData(BaseModel): 
    id: int 

class Vote(BaseModel): 
    post_id: int
    voted: bool 

