#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.model_registry import mapped_classes
import unittest
from configs.env_vars import HBNB_TYPE_STORAGE


class test_User(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'User'
        self.value = mapped_classes['User']

    def test_first_name(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'first_name'))

    def test_last_name(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'last_name'))

    def test_email(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'email'))

    def test_password(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'password'))

    def test_places_class_attrbute(self):
        self.assertTrue(hasattr(self.value, 'places'))

    def test_reviews_attr(self):
        self.assertTrue(hasattr(self.value, 'reviews'))

    @unittest.skipIf(HBNB_TYPE_STORAGE != 'db', reason='Requires database')
    def test_table_name(self):
        """ """
        self.assertEqual(self.value.__tablename__, 'users')
