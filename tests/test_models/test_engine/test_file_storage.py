#!/usr/bin/python3
""" Module for testing file storage"""
import os
import unittest
from models import storage
from models.base_model import BaseModel
from unittest.mock import patch, MagicMock
from models.model_registry import mapped_classes
from configs.environment_variables import HBNB_TYPE_STORAGE


@unittest.skipIf(HBNB_TYPE_STORAGE != 'file', reason='Requires file storage')
class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]
        self.value = BaseModel

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = self.value()
        new.save()
        new.save()
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_all(self):
        """ __objects is properly returned """
        new = self.value()
        new.save()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = self.value()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = self.value()
        new.save()
        thing = new.to_dict()
        new.save()
        new2 = self.value(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = self.value()
        new.save()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = self.value()
        new.save()
        storage.reload()
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = self.value()
        new.save()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = self.value()
        new.save()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        print(type(storage))
        self.assertEqual(type(storage), FileStorage)

    @patch('models.engine.file_storage.FileStorage.all')
    def test_delete(self, mock_all):
        """Verify that obj is deleted from __objects"""
        from models.engine.file_storage import FileStorage
        fs = FileStorage()
        # create the mock instance and set it attributes
        mock_instance = MagicMock()
        mock_instance.__class__.__name__ = "ExistingClass"
        mock_instance.id = 1234
        key = "ExistingClass.1234"
        # store mock instance in dictionary
        mock_object = {key: mock_instance}
        # self.all() will return a dictionary that contains fake object
        mock_all.return_value = mock_object
        # act
        fs.delete(mock_instance)
        # check if the mock instance is deleted from the dictionary mock_object
        mock_all.assert_called_once()
        self.assertNotIn(key, mock_object)
        # check if it does nothing when obj is None
        mock_all.reset_mock()
        fs.delete(None)
        mock_all.assert_not_called()

    def test_all_is_called_with_class_name(self):
        """ Check if the method returns all object of a specific
        type
        """
        # create two object
        storage.new(self.value())
        storage.new(MagicMock())

        # check if the object returned is of type BaseModel
        for obj in storage.all(self.value).values():
            self.assertIsInstance(obj, self.value)

    def test_state_city_integration(self):
        """Test that relationship between State and City is established"""
        state = mapped_classes['State']()

        city1 = mapped_classes['City']()
        city1.state_id = state.id
        city1.save()

        city2 = mapped_classes['City']()
        city2.state_id = state.id
        city2.save()

        self.assertIn(city1, state.cities)
        self.assertIn(city2, state.cities)
