#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    # Define common class attributes or columns for the table
    id = Column(String(60), default=str(uuid.uuid4()), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instanciate a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                    # convert from ISO string format to datetime
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__':
                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        attr_dict = self.__dict__

        if '_sa_instance_state' in self.__dict__:
            attr_dict = self.__dict__.copy()
            attr_dict.pop('_sa_instance_state')
        return '[{}] ({}) {}'.format(cls, self.id, attr_dict)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        state_key = '_sa_instance_state'
        if state_key in dictionary:
            dictionary.pop(state_key)

        return dictionary

    def delete(self):
        models.storage.delete(self)
