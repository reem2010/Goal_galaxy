#!/usr/bin/python3
"""
initialize the models package
"""
from data.engine.storage import DBStorage
storage = DBStorage()
storage.reload()