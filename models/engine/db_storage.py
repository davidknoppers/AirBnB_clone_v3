#!/usr/bin/python3
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import (sessionmaker, scoped_session)
from os import getenv
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
"""
This is the db_storage module
"""


class DBStorage:
    __engine = None
    __session = None
    __Session = None

    def __init__(self):
        """
        initializes engine
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')))
        self.__models_available = {"User": User,
                                   "Amenity": Amenity, "City": City,
                                   "Place": Place, "Review": Review,
                                   "State": State}
        if getenv('HBNB_MYSQL_ENV', 'not') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        returns a dictionary of all the class objects
        """
        orm_objects = {}
        if cls:
            for k in self.__session.query(self.__models_available[cls]):
                orm_objects[k.__dict__['id']] = k
        else:
            for i in self.__models_available.values():
                j = self.__session.query(i).all()
                if j:
                    for k in j:
                        orm_objects[k.__dict__['id']] = k
        return orm_objects

    def count(self, cls=None):
        """
        returns count of a class if one is specified or just counts all objects
        """
        #if class is valid, set up a sqlalchemy query to return count
        if cls:
            if cls not in self.__models_available.keys():
                return None
            else:
                cls_name = self.__models_available[cls]
                return (self.__session.query(cls_name).count())
        #return length of all if no class was passed
        return (len(self.all()))

    def get(self, cls, _id):
        """
        returns object based on class name and ID
        """
        if cls not in self.__models_available.keys():
            return None
        cls_name = self.__models_available[cls]
        return (self.__session.query(cls_name).get(_id))

    def new(self, obj):
        """
        adds a new obj to the session
        """
        self.__session.add(obj)

    def save(self):
        """
        saves the objects fom the current session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes an object from the current session
        """
        if obj is not None:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        """
        WARNING!!!! I'm not sure if Base.metadata.create_all needs to
        be in the init method
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def close(self):
        """
        close a session
        """
        self.__session.remove()
