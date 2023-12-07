#!/usr/bin/python3

import console
import pep8
import unittest

HBNBCommand = console.HBNBCommand

class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""

    def _test_pep8_conformance(self, file_path):
        """Test that a given file conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files([file_path])
        self.assertEqual(result.total_errors, 0,
                         f"Found PEP8 code style errors in {file_path}")

    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        self._test_pep8_conformance('console.py')

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        self._test_pep8_conformance('tests/test_console.py')

    def _test_module_class_docstring(self, module_class, entity_name):
        """Test docstring presence and length for a module or class."""
        entity = getattr(console, module_class)
        self.assertIsNot(entity.__doc__, None,
                         f"{entity_name} needs a docstring")
        self.assertTrue(len(entity.__doc__) >= 1,
                        f"{entity_name} needs a docstring")

    def test_module_class_docstring(self):
        """Test for console.py and HBNBCommand class docstrings"""
        self._test_module_class_docstring('HBNBCommand', 'HBNBCommand')
        self._test_module_class_docstring('console', 'console')

