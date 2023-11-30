#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, String, Column  
Base = declarative_base()

time = "%Y-%m-%dT%H:%M:%S.%f"
class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
       
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

 

    def save(self):
        """Updates updated_at with current time when instance is changed"""

        from data import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Create dictionary of object"""

        update_dict = (self.__dict__).copy()
        update_dict['created_at'] = self.created_at.isoformat()
        update_dict['updated_at'] = self.updated_at.isoformat()
        return update_dict

    def delete(self):
        """delete the current instance from the storage"""
        from data import storage

        storage.delete(self)