#!/usr/bin/python3
"""New engine for data base storage"""
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from data.base import BaseModel, Base
from data.task import Task
from data.user import User


class DBStorage:
    """clasee for the New engine"""
    __engine = None
    __session = None

    def __init__(self):
        """initializing a new instance"""

        user = os.environ.get('todo_USER')
        password = os.environ.get('todo_PWD')
        host = os.environ.get('todo_HOST')
        database = os.environ.get('todo_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, password, host, database), pool_pre_ping=True)

    def all(self, cls=None, id=0):
        """query objects"""
        classes = []
        data = []
        tables = {}
        if id:
            data = self.__session.query(Task).filter(Task.user_id == id).all()
        else:
           data = self.__session.query(User).all()
        for i in data:
            key = f"{i.__class__.__name__}.{i.id}"
            tables[key] = i
        return tables
    
    def priority(self, id):
        """orderd by priority"""
        tables = {}
        data = self.__session.query(Task).filter(Task.user_id == id).order_by(Task.priority.desc()).all()
        for i in data:
            key = f"{i.__class__.__name__}.{i.id}"
            tables[key] = i
        return tables
    

    def deadline(self, id):
        """orderd by deadline"""
        tables = {}
        data = self.__session.query(Task).filter(Task.user_id == id).order_by(Task.deadline).all()
        for i in data:
            key = f"{i.__class__.__name__}.{i.id}"
            tables[key] = i
        return tables
    
    
    def new(self, obj):
        """add new obj"""
        self.__session.add(obj)

    def save(self):
        """save to data base"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        """reload data base"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)()

    def close(self):
        """close a sessiom"""
        self.__session.close()