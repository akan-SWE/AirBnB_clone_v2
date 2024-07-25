#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from configs.env_vars import HBNB_TYPE_STORAGE
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table


class Place(BaseModel, Base):
    """A place to stay

    Attributes:
        __tablename__: represents table name of the MySQL table to store users
        city_id: represents a column containing a string(60 Characters).
            Can't be null, and is a foreign key to cities.id
        user.id: represents a column containing a string(60 Characters).
            Can't be null, and is a foreign key to users.id
        name: represents a column containing a string(128 characters).
            Can't be null
        description: represents a column containing a string(1024 characters)
        number_rooms: represents a column containing an integer.
            Can't be null. Default: 0.
        number_bathrooms: represents a column containing an integer.
            Can't be null. Default: 0.
        max_guest: represents a column containing an integer.
            Can't be null. Default: 0.
        price_by_night: represents a column containing an integer.
            Can't be null. Default 0.
        latitude: represents a column containing a float. Can be null
        longitude: represents a column containing a float. Can be null
    """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    def __init__(self, *args, **kwargs):
        """
        Initialize an Place instance.

        Handles differences in initialization based on the storage type.
        """
        if HBNB_TYPE_STORAGE == 'db':
            BaseModel.__init__(self)
            Base.__init__(self, *args, **kwargs)
        else:
            BaseModel.__init__(self, *args, **kwargs)

    if HBNB_TYPE_STORAGE == 'db':
        reviews = relationship('Review', backref='place',
                               cascade='all, delete')
        amenities = relationship('Amenity', secondary='place_amenity',
                                 back_populates='place_amenities')
    else:
        @property
        def reviews(self):
            """
            Returns the list of Review instances with place_id equals to the
            current Place object id
            """
            from models import storage
            from models.model_registry import mapped_classes

            Review = mapped_classes['Review']
            return [obj for obj in storage.all().values()
                    if isinstance(obj, Review) and obj.place_id == self.id]

        @property
        def amenities(self):
            """
            Returns the list of Amenity instances with ids in amenity_ids
            """
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj):
            """
            Handles the addition of an Amenity id to amenity_ids list
            """
            from models.model_registry import mapped_classes

            Amenity = mapped_classes['Amenity']
            if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)


# Associate table for the many to many relationship between Amentity and Place
place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
)
