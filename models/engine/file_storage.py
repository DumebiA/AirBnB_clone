#!/usr/bin/python3
"""This module defines the FileStorage class."""

import json
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

valid_classes = {
    "BaseModel": BaseModel,
    "User": User,
    "Place": Place,
    "Amenity": Amenity,
    "City": City,
    "Review": Review,
    "State": State
}


class FileStorage:
    """The file storage engine serializes and
    deserializes instances to a JSON file
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the objects dictionary"""
        return type(self).__objects

    def new(self, obj):
        """Sets new one in __objects dictionary."""
        if obj.id in type(self).__objects:
            print("exists")
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        type(self).__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON __file_path)"""
        obj_dict = []
        for obj in type(self).__objects.values():
            obj_dict.append(obj.to_dict())
        with open(type(self).__file_path, "w", encoding='utf-8') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects if it exists"""
        if os.path.exists(type(self).__file_path):
            try:
                with open(type(self).__file_path, "r") as file:
                    loaded_objects = json.load(file)
                    for val in loaded_objects:
                        key = "{}.{}".format(val['__class__'], val['id'])
                        obj = valid_classes[val['__class__']](**val)
                        type(self).__objects[key] = obj
            except Exception as e:
                print("Error reloading data:", e)
