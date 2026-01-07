from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

# to get a string like this run:
# openssl rand -hex 32
SECRET = "07e466554f8e8c30f972209cabb4c3a4b2e9a6f2fffb7a663cea71f9dbd08737"
ALGORITHM = "HS256" 
ACCESS_TOKEN_DURATION = 1

router = APIRouter(prefix="/jwtauth", 
                   tags=["jwtauth"],
                   responses={404: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

#Entidad user
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mourede.com",
        "disabled": False,
        "password":"$2a$12$XfdeAzqTABxf86i6UZLzQeinIycjBxeh9bmV6Fu2DF6OPqINRMByi"
        },
        "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure@mourede.com",
        "disabled": True,
        "password":"$2a$12$TCItrcgRhV3yCkV5OzEIXuEp6m9.LjrgzDF0Ct.NvBpxA0ydUwql."
        }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas", 
            headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    
    except JWTError:
        raise exception
    
    return search_user(username)



async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La contraseña no es correcta")
    

    access_token = {"sub":user.username, 
                    "exp":datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM) , "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user