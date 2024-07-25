#!/usr/bin/python3
""" """
from configs.env_vars import HBNB_TYPE_STORAGE
from models.base_model import BaseModel
from sqlalchemy import Column
from unittest.mock import patch, MagicMock
import unittest
from datetime import datetime
from uuid import UUID
from models import storage
import json
import os


# models.storage._FileStorage__objects = {}
class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        storage._FileStorage__objects = {}
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_default(self):
        """ """
        i = self.value()
        self.assertIsInstance(i, self.value)

    @unittest.skipIf(HBNB_TYPE_STORAGE == 'db', reason='Requires file storage')
    def test_kwargs(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        new = self.value(**copy)
        self.assertDictEqual(new.to_dict(), copy)

    def test_kwargs_int(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    @patch('models.storage.new')
    @patch('models.storage.save')
    def test_save(self, mock_save, mock_new):
        new = self.value()
        new.save()
        mock_new.assert_called_once()
        mock_save.assert_called_once()

    def test_str(self):
        """ """
        i = self.value()
        if '_sa_instance_state' in i.__dict__:
            i.__dict__.pop('_sa_instance_state')
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ """
        i = self.value()
        i._sa_instance_state = MagicMock()
        n = i.to_dict()
        self.assertTrue(hasattr(i, '_sa_instance_state'))
        self.assertNotIn('_sa_instance_state', n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    @unittest.skipIf(HBNB_TYPE_STORAGE == 'db', reason='Requires file storage')
    def test_kwargs_one(self):
        """ """
        n = {'Name': 'Test'}
        new = self.value(**n)

    @patch('models.storage.delete')
    def test_delete(self, mock_delete):
        new = self.value()
        new.delete()
        mock_delete.assert_called_once()

    def test_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

    def test_id_column_exists(self):
        """Test that the id is a Column object"""
        self.assertIsInstance(BaseModel.id, Column)

    def test_created_at_column_exist(self):
        """Test that created_at is a Column object"""
        self.assertIsInstance(BaseModel.created_at, Column)

    def test_updated_at_column_exist(self):
        """Test that updated_at is a Column object"""
        self.assertIsInstance(BaseModel.updated_at, Column)
