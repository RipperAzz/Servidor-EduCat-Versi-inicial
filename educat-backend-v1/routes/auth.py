from fastapi import APIRouter, HTTPException, Form, Depends, Request
from config.db import SessionLocal
from models.user import UserTable, TokenRefresh
from core.secure import verify_pswd, create_access_token, get_current_user, create_refresh_token
from schemas.user import LoginData
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_oauth")
auth_ = APIRouter()

@auth_.post("/login", response_model=dict, tags=["Authentication"])
def request_login(data: LoginData, request:Request):
    addr = request.client.host
    client_device = request.headers.get("User-Agent")
    with SessionLocal() as db:
        db_user = db.query(UserTable).filter(UserTable.email == data.email).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not verify_pswd(data.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid Credentials")
        
        token = create_access_token({"sub": db_user.public_id, "role": db_user.role})
        refresh_token = create_refresh_token({"sub": str(db_user.public_id), "addr": addr, "device": client_device})
        db_refresh_token = TokenRefresh(
            user_id = db_user.public_id,
            refresh_token=refresh_token,
            role = db_user.role,
            ip_addr = addr,
            device = client_device
            )
        db.add(db_refresh_token)
        db.commit()
        return {"access_token": token, "refresh_token": refresh_token, "token_type": "bearer"}
    
@auth_.post("/login_oauth", tags=["Authentication"])
def login_oauth(username: str = Form(...), password: str = Form(...)):
    with SessionLocal() as db:
        db_user = db.query(UserTable).filter(UserTable.username == username).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_pswd(password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid Credentials")
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}

@auth_.post("/refresh", tags=["Authentication"])
def refresh_token(data: dict, request: Request):
    client_device = request.headers.get("User-Agent")
    addr = request.client.host
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token required")
    with SessionLocal() as db:
        db_token = db.query(TokenRefresh).filter(refresh_token == TokenRefresh.refresh_token).first()
        db_user = db.query(UserTable).filter(UserTable.public_id == db_token.user_id).first()
        if not db_token or db_token.revocated or db_token.expired_at < datetime.now():
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        if db_token.device != client_device:
            raise HTTPException(status_code=401, detail="Token not valid for this device/IP")
        if db_token.ip_addr != addr:
            print(f"Alerta: refresh token usado desde IP distinta: {addr}")

        new_acces_token = create_access_token({"sub": db_user.public_id, "role": db_user.role})
        return {"access_token": new_acces_token, "token_type": "bearer"}
        
@auth_.get("/protected")
def protected_route(user_data: dict = Depends(get_current_user)):
    return {"message": f"Hola {user_data}, esta ruta está protegida"}