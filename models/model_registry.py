#!/usr/bin/env python3
"""
Module: model_registry

Stores all classes of the database schema in a dictionary for use
throughout the program.
"""
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

mapped_classes = {
    'State': State, 'City': City
}
