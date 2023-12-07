#!/usr/bin/python3

import re
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from shlex import split
import argparse

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    all_classes = {"BaseModel", "User", "State", "City", "Amenity", "Place", "Review"}

    def emptyline(self):
        pass

    def do_quit(self, line):
        return True

    def do_EOF(self, line):
        return True

    def do_create(self, line):
        if not line:
            print("** class name missing **")
            return

        class_name, *args = split(line)
        if class_name not in self.all_classes:
            print("** class doesn't exist **")
            return

        obj = eval(f"{class_name}()")
        for arg in args:
            match = re.match(r'^(\S+)=(\S+)', arg)
            if match:
                key, value = match.groups()
                value = value.strip('"').replace('_', ' ')
                if re.fullmatch(r'\d+', value):
                    value = int(value)
                elif re.fullmatch(r'\d+\.\d+', value):
                    value = float(value)
                setattr(obj, key, value)

        obj.save()
        print(obj.id)

    def do_show(self, line):
        if not line:
            print("** class name missing **")
            return

        class_name, *rest = split(line)
        if class_name not in storage.classes() or not rest:
            print("** instance id missing **")
            return

        obj_key = f"{class_name}.{rest[0]}"
        all_objects = storage.all()
        if obj_key not in all_objects:
            print("** no instance found **")
            return

        print(all_objects[obj_key])

    def do_destroy(self, line):
        if not line:
            print("** class name missing **")
            return

        class_name, *rest = split(line)
        if class_name not in storage.classes() or not rest:
            print("** instance id missing **")
            return

        obj_key = f"{class_name}.{rest[0]}"
        all_objects = storage.all()
        if obj_key in all_objects:
            del all_objects[obj_key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, line):
        class_name, *_ = split(line)
        if not line or class_name not in self.all_classes:
            print("** class doesn't exist **")
            return

        objs = [str(obj) for obj in storage.all().values() if obj.__class__.__name__ == class_name]
        print(objs)

    def do_update(self, line):
        if not line:
            print("** class name missing **")
            return

        args = split(line)
        if args[0] not in storage.classes() or len(args) < 2:
            print("** instance id missing **")
            return

        obj_key = f"{args[0]}.{args[1]}"
        all_objects = storage.all()
        if obj_key not in all_objects or len(args) < 3:
            print("** no instance found **")
            return

        obj = all_objects[obj_key]
        if len(args) < 4:
            print("** attribute name missing **")
            return

        attr_name = args[2]
        attr_value = args[3].strip('"').replace('_', ' ')

        if re.fullmatch(r'\d+', attr_value):
            attr_value = int(attr_value)
        elif re.fullmatch(r'\d+\.\d+', attr_value):
            attr_value = float(attr_value)

        setattr(obj, attr_name, attr_value)
        obj.save()

    def count(self, line):
        class_name, *_ = split(line)
        if not line or class_name not in self.all_classes:
            print("** class doesn't exist **")
            return

        objs = [obj for obj in storage.all().values() if obj.__class__.__name__ == class_name]
        print(len(objs))

    def default(self, line):
        parser = argparse.ArgumentParser()
        parser.add_argument('class_method', type=str)
        args = parser.parse_args(line.split('.'))
        class_method = args.class_method

        if class_method.endswith("()"):
            method_name = class_method[:-2]
            if hasattr(self, method_name):
                getattr(self, method_name)(line.split()[0])
        else:
            cmd.Cmd.default(self, line)

if __name__ == '__main__':
    HBNBCommand().cmdloop()
