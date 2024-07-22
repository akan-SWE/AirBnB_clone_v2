#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.place import Place
import unittest
from configs.env_vars import HBNB_TYPE_STORAGE
from models.model_registry import mapped_classes


class test_Place(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'Place'
        self.value = mapped_classes['Place']

    def test_city_id(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'city_id'))

    def test_user_id(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'user_id'))

    def test_name(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'name'))

    def test_description(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'description'))

    def test_number_rooms(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'number_rooms'))

    def test_number_bathrooms(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'number_bathrooms'))

    def test_max_guest(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'max_guest'))

    def test_price_by_night(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'price_by_night'))

    def test_latitude(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'latitude'))

    def test_longitude(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'longitude'))

    def test_amenity_ids(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'amenity_ids'))


    @unittest.skipIf(HBNB_TYPE_STORAGE != 'db', reason='Requires database storage')
    def test_table_name(self):
        """ """
        self.assertEqual(self.value.__tablename__, 'places')

    def test_user_attr(self):
        """ """
        new = self.value()
        # print(new.places)
        self.assertTrue(hasattr(self.value, 'user'))

        # user = User()


        # print(User)
