from passlib.context import CryptContext 
from jose import JWTError, jwt 
from datetime import datetime, timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer 
from fastapi import Depends, status, HTTPException
from . import schemas
from .settings import environment_vars

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = environment_vars.secret_key
ALGORITHM = environment_vars.algo
ACCESS_TOKEN_EXPIRE_MINUTES = environment_vars.access_token_minute

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def createhashedpass(password: str): 
    return pwd_context.hash(password) 

def verifypassword(plain_password, hashed_password): 
    return pwd_context.verify(plain_password, hashed_password) 

def createtoken(userdata: dict): 
    to_encode = userdata.copy() 
    exp_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": exp_time})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 
    return access_token

def verifytoken(token: str, credentials_exception): 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if not user_id: 
            raise credentials_exception 
        #user_id = schemas.TokenData
    except JWTError: 
        raise credentials_exception 
    return user_id
    
def getcurrent_user(token: str = Depends(oauth2_scheme)): 
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized", headers={"WWW-Authenticate": "Bearer"})
    return verifytoken(token, credentials_exception)