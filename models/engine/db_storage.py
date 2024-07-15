#!/usr/bin/python3
"""
Module: db_storage

Defines the DBStorage class, which manages the database storage engine
and facilitates basic operations on database objects.

Note: This class is designed to work only with classes that are part of the
database schema.
"""
from models.model_registry import mapped_classes
from models.base_model import Base
from sqlalchemy.orm import sessionmaker


class DBStorage:
    """
    Defines a database storage engine.

    Attributes:
        __engine (sqlalchemy.engine.Engine): Connection to the database.
        __session (sqlalchemy.orm.session.Session): Maintains a session to
            interact with the database.

    Methods:
        __init__(): Creates a new database engine.
        all(cls=None): Returns a dictionary of all objects of a given class.
            If no class is specified, returns all objects in the database.
        new(obj): Adds a new object to the current database session.
        save(): Commits the current session to the database.
        delete(obj): Deletes an object from the current database session.
        reload(): Initializes the session and creates tables in the database
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes a new database engine."""
        from sqlalchemy.engine.url import URL
        from configs import env_vars
        from sqlalchemy import create_engine

        mysqldb_info = {
            'drivername': 'mysql+mysqldb',
            'username': env_vars.HBNB_MYSQL_USER,
            'password': env_vars.HBNB_MYSQL_PWD,
            'host': env_vars.HBNB_MYSQL_HOST,
            'database': env_vars.HBNB_MYSQL_DB
        }
        self.__engine = create_engine(str(URL.create(**mysqldb_info)),
                                      pool_pre_ping=True)
        # In test environment, delete all tables to start with fresh data
        if env_vars.HBNB_ENV == "test":
            Base.metadata.reflect(bind=self.__engine)
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of all objects of a given class.
        If no class is specified, returns all objects in the database.

        Parameters:
            cls (type, optional): The class of objects to return.
                If not specified, returns all objects in the database.

        Returns:
            dict: A dictionary of all objects of the specified class or all
                objects in the database.
        """
        with self.Session() as session:
            # use class passed or all classes if None is passed
            classes_to_query = [cls] if cls else mapped_classes.values()
            # Add objects of the classes
            objs_dict = {}
            for cls in classes_to_query:
                objs = self.__session.query(cls).all()
                if len(objs) > 0:
                    objs_dict.update({f'{type(obj).__name__}.{obj.id}':
                                      obj for obj in objs})
            return objs_dict

    def new(self, obj):
        """
        Adds a new object to the current database session.
        The object must be an instance of a class that is part of the
        database schema.

        Parameters:
            obj (object): The object to add to the session.
                It must be an instance of a class defined in the
                database schema.

        Returns:
            None
        """
        with self.Session() as session:
            self.__session.add(obj)

    def save(self):
        """
        Commits the current session to the database.

        This method saves all changes made to the objects in the
        current session to the database.

        Returns:
            None
        """
        with self.Session() as session:
            self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the current database session.

        Parameters:
            obj (object): The object to delete from the database session.
            It must be an instance of a class defined in the database schema.

        Returns:
            None
        """
        with self.Session() as session:
            if obj:
                self.__session.delete(obj)

    def reload(self):
        """
        Initializes the session and creates a new table if it doesn't exist
        in the database.

        This method should be called before any operations are performed on
        the database to ensure that the necessary tables and session are
        set up.

        Returns:
            None
        """
        Base.metadata.create_all(bind=self.__engine)
        self.Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = self.Session()
