#!/usr/bin/python3
"""This module defines a class User"""
from data.base import BaseModel, Base
from sqlalchemy import ForeignKey, String, Column, Integer, DateTime
from sqlalchemy.orm import relationship


class Task(BaseModel, Base):
    """This class defines the tasks"""

    __tablename__ = "tasks"
    name = Column(String(128), nullable=False)
    priority = Column(Integer, default=1)
    deadline = Column(DateTime, nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)