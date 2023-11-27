#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, String, Column  
Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if 'id' not in kwargs.keys():
                self.id = str(uuid.uuid4())
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key == "created_at" or key == "updated_at":
                    if key == "created_at":
                        self.created_at = datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%f"
                        )
                    else:
                        self.updated_at = datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%f"
                        )
                else:
                    setattr(self, key, value)


    def save(self):
        """Updates updated_at with current time when instance is changed"""

        from data import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def delete(self):
        """delete the current instance from the storage"""
        from data import storage

        storage.delete(self)