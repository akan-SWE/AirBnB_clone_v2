#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base, Column, String
from configs.env_vars import HBNB_TYPE_STORAGE
from sqlalchemy import ForeignKey


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False,)

    def __init__(self, *args, **kwargs):
        """
        Initialize an City instance.

        Handles differences in initialization based on the storage type.
        """
        if HBNB_TYPE_STORAGE == 'db':
            BaseModel.__init__(self)
            Base.__init__(self, *args, **kwargs)
        else:
            BaseModel.__init__(self, *args, **kwargs)
