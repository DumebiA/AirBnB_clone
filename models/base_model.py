#!/usr/bin/python3

import uuid
from datetime import datetime
import models


class BaseModel:
    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.
        Assigns a unique id, created_at, and updated_at attributes.
        """
        if kwargs:
            dat_format = '%Y-%m-%dT%H:%M:%S.%f'
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                elif key == 'created_at':
                    self.created_at = datetime.strptime(
                        kwargs['created_at'], dat_format)
                elif key == 'updated_at':
                    self.updated_at = datetime.strptime(
                        kwargs['updated_at'], dat_format)
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.
        Format: "[<class name>] (<self.id>) <self.__dict__>"
        """
        clsName = self.__class__.__name__
        return "[{}] ({}) {}".format(clsName, self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute
        updated_at with the current datetime.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all
        keys/values of __dict__ of the instance.
        Adds a key __class__ with the class name of the object.
        Converts created_at and updated_at to
        string objects in ISO format.
        This method is the first piece of the
        serialization/deserialization process.
        """
        obj_dict = self.__dict__.copy()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['__class__'] = self.__class__.__name__
        return obj_dict
