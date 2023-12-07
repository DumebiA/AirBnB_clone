#!/usr/bin/python3
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, DateTime, Column
import models

Base = declarative_base()

class BaseModel:
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            time = datetime.now()
            if "created_at" not in kwargs:
                self.created_at = time
            if "updated_at" not in kwargs:
                self.updated_at = time
        else:
            self.id = str(uuid.uuid4())
            time = datetime.now()
            self.created_at = time
            self.updated_at = time

    def __str__(self):
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.to_dict())

    def __repr__(self):
        return self.__str__()

    def save(self):
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy instance state if present
        return my_dict

    def delete(self):
        models.storage.delete(self)

