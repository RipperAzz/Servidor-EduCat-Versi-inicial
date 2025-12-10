from fastapi import APIRouter, HTTPException, Response, Depends, Request, UploadFile, File
from config.db import SessionLocal
from core.secure import get_pswd_hash, verify_pswd, require_role, get_current_user
from models.user import UserTable
import starlette.status as s
from schemas.user import Users, UserUpdate, Password_new
user = APIRouter()
messages = []
@user.get("/users", tags=["Admin"])
def get_users(user_role: dict = Depends(require_role(["Admin"]))):
    with SessionLocal() as Session:
        users = Session.query(UserTable).all()
        if users:
            return users
        return {"message": "No users yet"}
    
@user.post("/users", tags=["Users"])
def create_user(user : Users):
    with SessionLocal() as Session:
        exists = Session.query(UserTable).filter(UserTable.username == user.username).first()
        if exists is None:
            new_user = UserTable(username=user.username, password=get_pswd_hash(user.password), email=user.email, role=user.role)
            Session.add(new_user)
            Session.commit()
            return {"Success": "The user has been added"}    
        raise HTTPException(status_code=403, detail="The user already exists")

@user.get("/users/u/{username}", tags=["Users"])
def public_porfile(username: str):
    with SessionLocal() as Session:
        try:
            user = Session.query(UserTable).filter(UserTable.username == username).one()
            return {"username": user.username, "role": user.role, "created_at": user.created_at}
        except:
            raise HTTPException(status_code=400, detail="User has not found")

@user.get("/users/id/{public_id}", tags=["Users"])
def get_user(public_id: str, user_role: dict = Depends(require_role(["Admin"]))):
    with SessionLocal() as Session:
        try:
            user = Session.query(UserTable).filter(UserTable.public_id == public_id).one()
            return {"username": user.username, "role": user.role, "created_at": user.created_at}
        except:
            raise HTTPException(status_code=400, detail="User has not found")

@user.delete("/users/id/{public_id}", status_code=s.HTTP_204_NO_CONTENT, tags=["Admin"])
def delete_user(public_id:str, user_role: dict = Depends(require_role(["Admin"]))):
    with SessionLocal() as Session:
        Session.query(UserTable).filter(UserTable.public_id == public_id).delete()
        Session.commit()
        return Response(status_code=s.HTTP_204_NO_CONTENT)

@user.put("/users/me", tags=["Users"])
def profile_update(userUp: UserUpdate,user=Depends(get_current_user)):
    with SessionLocal() as Session:
        user_update = Session.query(UserTable).filter(UserTable.public_id == user["sub"]).first()
        if not user_update:
            raise HTTPException(status_code=404,detail="User not found")
        if userUp.email is not None:
            user_update.email = userUp.email
        if userUp.username is not None:
            user_update.username = userUp.username
        Session.commit()
    return {"Uploadad": "User has been updated"}

@user.post("/users/me/post",tags=["Users"])
def post_file(user=Depends(get_current_user), file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=422, detail="Invalid fromat, hacking?")
    return {"message": "File accepted"}
    
@user.put("/users/me/password", tags=["Users"])
def change_pass(password: Password_new,user=Depends(get_current_user)):
    with SessionLocal() as Session:
        _user_pass_update = Session.query(UserTable).filter(UserTable.public_id == user["sub"]).first()
        if not _user_pass_update:
            raise HTTPException(status_code=404,detail="User not found")
        
        if not verify_pswd(password.oldPass, _user_pass_update.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if verify_pswd(password.newPass, _user_pass_update.password):
            raise HTTPException(status_code=400, detail="New password cannot be the same as the old one")
        
        _user_pass_update.password = get_pswd_hash(password.newPass)
        Session.commit()
    return {"message": "User password has been updated"}