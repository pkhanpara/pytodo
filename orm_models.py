from sqlalchemy import Column, String, Boolean, ForeignKey
# Using String to store UUIDs for SQLite compatibility
from sqlalchemy.orm import relationship
import uuid
from database import Base

class List(Base):
    __tablename__ = "lists"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    items = relationship("Item", back_populates="list", cascade="all, delete-orphan")

class Item(Base):
    __tablename__ = "items"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    checkmark = Column(Boolean, default=False)
    list_id = Column(String, ForeignKey("lists.id"), nullable=False)
    list = relationship("List", back_populates="items")
