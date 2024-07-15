#!/usr/bin/python3
""" """
from models import storage
from models.model_registry import mapped_classes
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import InstrumentedAttribute
from configs.environment_variables import HBNB_TYPE_STORAGE
from tests.test_models.test_base_model import test_basemodel, unittest


class test_state(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        self.name = "State"
        self.value = mapped_classes['State']
        super().__init__(*args, **kwargs)

    def test_tablename_column_exists(self):
        self.assertEqual(self.value.__tablename__, 'states')

    @unittest.skipIf(HBNB_TYPE_STORAGE != 'db', reason="Requires db storage")
    def test_name_column_exists(self):
        self.assertIsInstance(self.value.name, InstrumentedAttribute)

    @unittest.skipIf(HBNB_TYPE_STORAGE != 'db', reason="Requires db storage")
    def test_cities_column_exist_db(self):
        self.assertIsInstance(self.value.cities, InstrumentedAttribute)

    @patch('models.storage.all')
    @patch('models.storage._FileStorage__objects', new_callable=dict)
    @unittest.skipIf(HBNB_TYPE_STORAGE != 'file',
                     reason="Requires file storage")
    def test_cities_getters_filestorage(self, mock_objects, mock_all):
        """Test cities getters used for the file storage type"""
        from models.city import City

        state = mapped_classes['State']()

        mock_city = MagicMock(spec=City)
        mock_city.state_id = state.id
        mock_city.id = 123

        mock_objects["MOCKCITY.123"] = mock_city
        mock_all.return_value = mock_objects

        cities = state.cities
        self.assertIsInstance(cities, list)
        self.assertEqual(cities, [mock_city])
