from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timedelta
from .base import Base
from nanoid import generate
def default_expired_at():
    return datetime.now() + timedelta(days=30)

class UserTable(Base):
    __tablename__ = 'Users'
    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    public_id = Column(String(21), default=generate, nullable=False, unique=True, index=True)
    username = Column(String(40), nullable = False, unique =True, index=True)
    email = Column(String(50), nullable = False, index=True)
    role = Column(String(), default="student", nullable=False)    
    password = Column(String(255))
    created_at = Column(DateTime(), default=datetime.now)

    refresh_tokens = relationship("TokenRefresh", back_populates="user")

class TokenRefresh(Base):
    __tablename__ = 'token_refresh'
    token_id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(String(), ForeignKey("Users.public_id"), nullable=False)
    role = Column(String(), default="student", nullable=False) 
    refresh_token = Column(String(), nullable=False, unique=True)
    ip_addr = Column(String(), nullable=False)
    device = Column(String(), nullable=True)
    revocated = Column(Boolean(), default=False, nullable=False)
    expired_at = Column(DateTime(), default=default_expired_at)

    user = relationship("UserTable", back_populates="refresh_tokens")
