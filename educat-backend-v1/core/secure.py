from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt
from datetime import datetime, timedelta, timezone
from core.config import settings
bearer_scheme = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_pswd_hash(password:str) -> str:
    return pwd_context.hash(password)

def verify_pswd(plain_text: str, hash_pswd:str) -> bool:
    return pwd_context.verify(plain_text, hash_pswd)

def create_access_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    data["date"] = str(datetime.now(timezone.utc))
    data["exp"] = int(expire.timestamp())
    return jwt.encode(data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token:str) -> dict:
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired Token")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Token")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    user_data = verify_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_data

def require_role(requiredRoles: list[str]):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] not in requiredRoles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    return role_checker

def create_refresh_token(data: dict) -> str:
    data["date"] = str(datetime.now(timezone.utc))
    return jwt.encode(data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)