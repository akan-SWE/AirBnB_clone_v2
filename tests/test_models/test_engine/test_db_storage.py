#!/usr/bin/python3
"""
Module: test_db_storage

Defines test cases for the DBStorage class.
"""

import unittest
from models import storage
from unittest.mock import patch, MagicMock
from models.engine.db_storage import DBStorage, Base
from configs.env_vars import HBNB_TYPE_STORAGE


@unittest.skipIf(HBNB_TYPE_STORAGE != 'db', reason='Requires database storage')
class test_DBStorage(unittest.TestCase):
    """
    Defines test cases for the DBStorage class.
    """
    @classmethod
    def setUpClass(cls):
        """Instantiate a database connection"""
        cls.conn = cls.create_connection()

    def setUp(self):
        """Creates a new cursor object"""
        self.cursor = self.conn.cursor()

    def tearDown(self):
        """Close cursor object"""
        self.cursor.close()

    def test_class_attributes_default_values(self):
        """
        Test that all class attributes are None as default
        """
        self.assertEqual(DBStorage._DBStorage__engine, None)
        self.assertEqual(DBStorage._DBStorage__session, None)

    def test_engine_configuration(self):
        """Test that the engine is created to the right database"""
        engine = storage._DBStorage__engine

        self.assertNotEqual(engine, None)
        self.assertEqual(engine.url.drivername, 'mysql+mysqldb')
        self.assertEqual(engine.url.username, 'hbnb_test')
        self.assertEqual(engine.url.password, 'hbnb_test_pwd')
        self.assertEqual(engine.url.host, 'localhost')
        self.assertEqual(engine.url.database, 'hbnb_test_db')

    @patch('models.base_model.Base.metadata.drop_all')
    def test_table_drop_on_test_env(self, mock_drop_all):
        """Test that drop_all() is called to delete all table on each test"""
        DBStorage()
        mock_drop_all.assert_called_once()

    def test_all_with_class(self):
        """Test that all correctly returns a list of all """
        with patch.object(storage._DBStorage__session, 'query') as mock_query:
            mock_obj = MagicMock()
            mock_query.all.return_value = [mock_obj]

            storage.all(mock_obj)
            mock_query.assert_called_once_with(mock_obj)

    def test_all_with_no_class(self):
        """Test that all returns all objects if no class is passed"""

        with patch.object(storage._DBStorage__session, 'query') as mock_query:
            mock_user = MagicMock()
            mock_place = MagicMock()
            mock_amenity = MagicMock()
            mock_review = MagicMock()
            mock_city = MagicMock()
            mock_state = MagicMock()

            mock_query.all.return_value = [mock_user, mock_place, mock_amenity,
                                           mock_review, mock_city, mock_state]
            storage.all(None)

            mock_query.assert_called()

    @patch.object(storage, '_DBStorage__session')
    def test_new_obj_creation(self, mock_session):
        """Test that new adds new object to the database session"""
        mock_obj = MagicMock()
        storage.new(mock_obj)
        mock_session.add.assert_called_once_with(mock_obj)

    @patch.object(storage, '_DBStorage__session')
    def test_save_changes(self, mock_session):
        """Test that save commit to the current database session"""
        storage.save()
        mock_session.commit.assert_called_once()

    @patch.object(storage, '_DBStorage__session')
    def test_delete_obj_not_None(self, mock_session):
        """Test that delete removes an object from the database session"""
        mock_obj = MagicMock()
        storage.delete(mock_obj)
        mock_session.delete.assert_called_once_with(mock_obj)

    @patch.object(storage, '_DBStorage__session')
    def test_delete_obj_None(self, mock_session):
        """Test that delete does nothing when None is passed"""
        storage.delete(None)
        mock_session.delete.assert_not_called()

    @patch('models.engine.db_storage.scoped_session')
    @patch('models.engine.db_storage.sessionmaker')
    @patch('models.engine.db_storage.Base.metadata.create_all')
    def test_reload(self, mock_create_all, mock_session, mock_scoped_session):
        """
        Test that reload properly creates new session and tables in the
        database
        """
        storage.reload()
        mock_create_all.assert_called_once()
        mock_session.assert_called_once()
        mock_scoped_session.assert_called_once()

    @patch.object(storage, '_DBStorage__session')
    def test_close(self, mock_session):
        self.assertTrue(hasattr(storage, 'close'))
        storage.close()
        mock_session.remove.assert_called_once()

    def test_integrations(self):
        """Testing the interactions between each methods of the class"""
        from models.model_registry import mapped_classes

        # get classes
        City = mapped_classes['City']
        State = mapped_classes['State']

        # create state and save to the table
        state = State()
        state.name = 'California'
        state.save()

        # create city and save to the table
        city1 = City()
        city1.name = 'Los Angeles'
        city1.state_id = state.id
        city1.save()

        city2 = City()
        city2.name = 'San Francisco'
        city2.state_id = state.id
        city2.save()

        self.assertIn(city1, state.cities)
        self.assertIn(city2, state.cities)

    @classmethod
    def create_connection(cls):
        """Creates a new connection with the database"""
        import MySQLdb
        from configs import env_vars

        conn = MySQLdb.connect(
            host=env_vars.HBNB_MYSQL_HOST,
            user=env_vars.HBNB_MYSQL_USER,
            passwd=env_vars.HBNB_MYSQL_PWD,
            db=env_vars.HBNB_MYSQL_DB,
        )
        return conn

    @classmethod
    def tearDownClass(cls):
        """Close the database connection"""
        storage.reload()
        cls.conn.close()
