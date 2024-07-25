#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy.orm import relationship
from configs.env_vars import HBNB_TYPE_STORAGE
from models.base_model import BaseModel, Base, Column, String


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    if HBNB_TYPE_STORAGE == 'db':
        cities = relationship('City', backref='state')
    else:
        @property
        def cities(self):
            """
            Returns the list of City instances with state_id equals to the
            current State object id
            """
            from models.model_registry import mapped_classes
            from models import storage

            City = mapped_classes['City']
            return [obj for obj in storage.all().values()
                    if isinstance(obj, City) and obj.state_id == self.id]

    def __init__(self, *args, **kwargs):
        """
        Initialize an State instance.

        Handles differences in initialization based on the storage type.
        """
        if HBNB_TYPE_STORAGE == 'db':
            BaseModel.__init__(self)
            Base.__init__(self, *args, **kwargs)
        else:
            BaseModel.__init__(self, *args, **kwargs)
