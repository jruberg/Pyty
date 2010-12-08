import unittest
import ast
import sys

# Include src in the Python search path.
sys.path.insert(0, '../src')

from typecheck import typecheck, parse_type_declarations
from pyty_types import PytyMod
from pyty_errors import VariableTypeUnspecifiedError

"""
This is just the core of the unit testing file. generate_tests.py must be run
to fill this file with the several unit tests (each of which tests one source
code file in the test_files directory).

Test file format:

### True|False|ErrorName

<Python code>
"""

class TestFileFormatError(Exception):
    """Exception subclass for error encountered when a test file is not
    specified correctly.

    @type msg: C{str}.
    @ivar msg: message specifying what in test file isn't specified correctly.
    """

    def __init__(msg):
       self.msg = msg

    def __str__(msg):
        return "TestFileFormatError: " + self.msg

class PytyTests(unittest.TestCase):

    def setUp(self):
        self.pyty_mod_obj = PytyMod()

    def _check_file(self, filename):

        env = parse_type_declarations(filename)

        with open(filename, 'r') as f:
            
            expected_str = f.readline().strip('###').strip()

            a = ast.parse(f.read())

            if expected_str == "True" or expected_str == "False":
                try:
                    # test if it's looking for a true or false value.
                    exp = ast.literal_eval(expected_str)

                    self.assertEqual(exp, typecheck(env, a, self.pyty_mod_obj))
                except VariableTypeUnspecifiedError:
                    self.fail("A variable type was not specified")

            elif expected_str == "VariableTypeUnspecifiedError":
                # test if it's looking for a VariableTypeUnspecifiedError. if
                # there end up being a lot of possible errors, might want to
                # generalize this, but if there are only going to be a couple,
                # might as well just include each case explicitly.
                self.assertRaises(VariableTypeUnspecifiedError, typecheck,
                        env, a, self.pyty_mod_obj)

            else:
                raise TestFileFormatError("Expected test value or error not \
                specified properly")


    ##### Generated unit tests will go below here
    ##### Generated unit tests will go above here

if __name__ == '__main__':
    unittest.main()

