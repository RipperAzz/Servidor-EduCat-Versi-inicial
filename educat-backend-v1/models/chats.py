from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Boolean, Text, REAL
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime, timedelta
import uuid

class Chat(Base):
    __tablename__ = "Chat"
    id = Column(String(), primary_key=True, default= lambda: str(uuid.uuid4().hex[:15]), unique=True, nullable=False)
    chats = relationship("UserChat", back_populates="user_chat")

class UsersChat(Base):
    __tablename__ = "UserChat"
    id = Column(Integer(),primary_key=True, autoincrement=True, nullable=False)
    chat = Column(Integer(), ForeignKey("Chat.id"))

    user_chat = relationship("Chat", back_populates="chats")

class Message(Base):
    __tablename__ = "Message"
    id = Column(Integer(),primary_key=True, autoincrement=True, nullable=False)
    chat_id = Column(Integer, ForeignKey("Chat.id"), nullable=False)
    content = Column(Text, nullable=True)
    file_url = Column(String, nullable=True)
    file_type = Column(String, nullable=True) 
    date_at = Column(DateTime(), default=datetime.now, nullable=False)

    chat = relationship("Chat", back_populates="chats")