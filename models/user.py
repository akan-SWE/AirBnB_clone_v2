#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel


class User(BaseModel, Base):
    """This class defines a user by various attributes.

    Attributes:
        __tablename__: represents table name of the MySQL table to store users
        email: represents a non-optional column containing a string(128 characters)
        password: represents a non-optional column containing a string(128 characters)
        first_name: represents optional column containing a string(128 characters)
        last_name: represents optional column containing a string(128 characters)

    """

    __tablename__ = 'users'

    email = Column(string(128), nullable=False)
    password = Column(string(128), nullable=False)
    first_name = Column(string(128), nullable=True)
    last_name = Column(string(128), nullable=True)
