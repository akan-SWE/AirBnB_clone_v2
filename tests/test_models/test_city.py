#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from sqlalchemy import Column
from models.city import City


class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_tablename_column_exist(self):
        """"""
        self.assertIsInstance(self.value.__tablename__, str)
        self.assertEqual(self.value.__tablename__, 'cities')

    def test_name_column_exists(self):
        """"""
        self.assertEqual(str(self.value.name), 'City.name')

    def test_state_id_column_exists(self):
        """"""
        self.assertEqual(str(self.value.state_id), 'City.state_id')
