#!/usr/bin/python3
""" """
from sqlalchemy.orm import InstrumentedAttribute
from models.model_registry import mapped_classes
from tests.test_models.test_base_model import test_basemodel


class test_Amenity(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'Amenity'
        self.value = mapped_classes['Amenity']

    def test_tablename_column_exist(self):
        """"""
        self.assertIsInstance(self.value.__tablename__, str)
        self.assertEqual(self.value.__tablename__, 'amenities')

    def test_name_column_exists(self):
        """ """
        self.assertTrue(hasattr(self.value, 'name'))

    # def test_place_amenities_exists(self):
    #     """ """
    #     self.assertTrue(hasattr(self.value, 'place_amenities'))
