#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from configs.env_vars import HBNB_TYPE_STORAGE


class Amenity(BaseModel, Base):
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Initialize an Amenity instance.

        Handles differences in initialization based on the storage type.
        """
        if HBNB_TYPE_STORAGE == 'db':
            BaseModel.__init__(self)
            Base.__init__(self, *args, **kwargs)
        else:
            BaseModel.__init__(self, *args, **kwargs)

    if HBNB_TYPE_STORAGE == 'db':
        place_amenities = relationship('Place', secondary='place_amenity',
                                       back_populates='amenities')
