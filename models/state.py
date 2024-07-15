#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.city import City
from sqlalchemy.orm import relationship
from configs.environment_variables import HBNB_TYPE_STORAGE
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
            current State.id
            """
            objs_instance = models.storage.all().values()
            related_cities = []
            for obj in objs_instance:
                if isinstance(obj, City):
                    if obj.state_id == self.id:
                        related_cities.append(obj)
            return related_cities

    def __init__(self, *args, **kwargs):
        BaseModel.__init__(self, *args, **kwargs)
        Base.__init__(self)
