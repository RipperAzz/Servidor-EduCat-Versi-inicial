from pydantic import BaseModel
from typing import Optional

class Users(BaseModel):
    username : str
    email : str
    password : str
    role : Optional[str] = None

class UserUpdate(BaseModel):
    username : Optional[str] = None
    email : Optional[str] = None

class Password_new(BaseModel):
    oldPass : str
    newPass : str

class LoginData(BaseModel):
    email: str
    password: str