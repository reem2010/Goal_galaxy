#!/usr/bin/python3
"""This module defines a class User"""
from data.base import BaseModel, Base
from sqlalchemy import ForeignKey, String, Column
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines the user"""

    __tablename__ = "users"
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False, unique=True)
    name = Column(String(128))
    tasks = relationship(
        "Task", cascade='all, delete, delete-orphan', backref="user")
    
    def password_validate(self, password):
        if self.password == password:
            return True
        else:
            return False