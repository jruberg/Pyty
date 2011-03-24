import unittest
import ast
import sys
import logging
from datetime import datetime
import ast

# Include src in the Python search path.
sys.path.insert(0, '../src')

from ast_extensions import *
from typecheck import *
from parse import *
from errors import *
import errors
from settings import *
from logger import Logger, announce_file

# these should be redundant, but they're necessary to refer to the specific log
# objects.
import ast_extensions
import parse
import typecheck

"""
This is just the core of the unit testing file. generate_tests.py must be run
to fill this file with the several unit tests (each of which tests one source
code file in the test_files directory).
"""

announce_file("unit_tests_core.py")

class PytyTests(unittest.TestCase):

    def _check_expr(self, s, expr_kind, type, expected):
        """Typechecks the string C{s} as an C{expr_type} expression."""

        a = ast.parse(s).body[0].value
            
        f = get_expr_func_name(expr_kind)

        if expected == "pass":
            self.assertEqual(True, call_function(f, a, type, {}),
                             "Should typecheck but does not (%s)." % s)
        elif expected == "fail":
            self.assertEqual(False, call_function(f, a, type, {}),
                             "Shouldn't typecheck but does. (%s)." % s)
        elif issubclass(getattr(errors, expected), PytyError):
            # if the expected value is an error, then make sure it
            # raises the right error.
            try:
                call_function(f, a, type, {})
            except getattr(errors, expected):
                pass
            else:
                self.fail("Should have raised error %s, but does not. (%s)."
                          % (expected, s))                
        else:
            raise TestFileFormatError("Expression tests can only be" + \
                " specified as passing, failing, or raising an error " + \
                " specified in errors.py, but this test was specified " + \
                " as expecting: " + expected)

    def _parse_and_check_mod(self, filename):
        with open(filename, 'r') as f:
            text = f.read()

        log = typecheck.log = parse.log = ast_extensions.log = Logger()

        debug_file = TEST_CODE_SUBDIR + DEBUG_SUBJECT_FILE
        if filename == debug_file:
            log.enter_debug_file()
        else:
            log.exit_debug_file()

        log.debug("\n---File text---\n" + text)

        untyped_ast = ast.parse(text)

        log.debug("\n---Untyped AST---\n" + str(untyped_ast), DEBUG_UNTYPED_AST)
            
        typedecs = parse_type_decs(filename)

        log.debug("\n---TypeDecs---\n" + str(typedecs), DEBUG_TYPEDECS)

        typed_ast = TypeDecASTModule(untyped_ast, typedecs)

        log.debug("\n---TypedAST---\n" + str(typed_ast), DEBUG_TYPED_AST)
            
        env_ast = EnvASTModule(typed_ast)

        logging.debug("\n---EnvAST---\n" + str(env_ast), DEBUG_ENV_AST)
            
        return check_mod(env_ast.tree)

    def _check_mod(self, filename):
        """Typechecks the contents of file C{filename} as a
        module. The file will contain a header of the form '### Pass'
        to indicate whether the module is expected to pass or fail
        typechecking or throw a specified error.
        """

        with open(filename, 'r') as f:
            expected = f.readline().strip('###').strip()
            text = f.read()

        if expected == "pass":
            # the third parameter is a message displayed if assertion fails.
            self.assertEqual(True, self._parse_and_check_mod(filename),
                             "Should typecheck, but does not:\n%s" % text)
        elif expected == "fail":
            # the third parameter is a message displayed if assertion fails.
            self.assertEqual(False, self._parse_and_check_mod(filename),
                             "Shouldn't typecheck, but does:\n%s" % text)
        elif issubclass(eval(expected), PytyError):
            try:
                result = self._parse_and_check_mod(filename)
            except getattr(errors, expected):
                pass
            else:
                self.fail("Should raise error %s, but instead returned %s:\n%s"
                          % (expected, result, text.strip('\n')))
        else:
            # in generate_tests.py, we should have already ensured that the
            # expecetd string is pass, fail, or a valid error name, so this case
            # should never be reached, but this is here just in case.
            raise Exception("Expected test result not specified with a " +
                            "valid value")
    

    ##### Generated unit tests will go below here
    ##### Generated unit tests will go above here

if __name__ == '__main__':
    unittest.main()

