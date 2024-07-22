#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user by various attributes.

    Attributes:
        __tablename__: represents table name of the MySQL table to store users
        email: represents a non-optional column containing a string(128 characters)
        password: represents a non-optional column containing a string(128 characters)
        first_name: represents optional column containing a string(128 characters)
        last_name: represents optional column containing a string(128 characters)
        places: represents a relation with the class Place.
        Description: All linked Place objects automatically delete if User object is deleted

    """

    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
