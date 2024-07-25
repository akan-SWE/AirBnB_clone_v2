#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from configs.env_vars import HBNB_TYPE_STORAGE
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = 'reviews'
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Initialize an Review instance.

        Handles differences in initialization based on the storage type.
        """
        if HBNB_TYPE_STORAGE == 'db':
            BaseModel.__init__(self)
            Base.__init__(self, *args, **kwargs)
        else:
            BaseModel.__init__(self, *args, **kwargs)
