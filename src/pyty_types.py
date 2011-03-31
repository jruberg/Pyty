import re

class PytyType:
    type_grammar = (PytyType._BaseType, PytyType._ParenType, PytyType._ListType,
                    PytyType._TupleType)
    
    class _BaseType:
        regex = r"^int|float|bool$"

        @staticmethod
        def matches(s):
            return re.match(PytyType._BaseType.regex, s) and True

        def __init__(self, s):
            self.s = s
            self.m = re.match(PytyType._BaseType.regex, s)

        def valid(self):
            return self.m

        def get_t(self):
            return self.s

        def get_members(self):
            return None
    
    class _ParenType:
        regex = r"^\((.*)\)$"

        @staticmethod
        def matches(s):
            return re.match(PytyType._ParenType.regex, s) and True
        
        def __init__(self, s):
            self.m = re.match(PytyType._ParenType.regex, s)
            if self.m:
                self.g = self.m.groups()

        def valid(self):
            return self.m and PytyType.valid(self.g[0])

        def get_t(self):
            if self.m:
                return PytyType(self.g[0]).t

            # should not be called on invalid input.
            assert(False)

        def get_members(self):
            if self.m:
                return PytyType(self.g[0]).members

            # should not be called on invalid input.
            assert(False)

    class _ListType:
        regex = r"^list of (.*)$"

        @staticmethod
        def matches(s):
            return re.match(PytyType._ListType.regex, s) and True

        def __init__(self, s):
            self.m = re.match(PytyType._ListType.regex, s)
            if self.m:
                self.g = self.m.groups()

        def valid(self):
            return self.m and PytyType.valid(self.g[0])

        def get_t(self):
            if self.m:
                return "list"

            # should not be called on invalid input.
            assert(False)

        def get_members(self):
            if self.m:
                return (PytyType(self.g[0]),)

            # should not be called on invalid input.
            assert(False)

    class _TupleType:
        regex = r"^((.*)\*)*(.*)$"

        @staticmethod
        def matches(s):
            return re.match(PytyType._TupleType.regex, s) and True

        def __init__(self, s):
            self.m = re.match(PytyType._TupleType.regex, s)
            if self.m:
                # XXX one potentially major caveat: this does not allow tuples
                # of tuples, since we're just counting the raw # of *'s.
                self.num_items = s.count("*") + 1

                self.g_regex = r"^" + r"(.*)\*" * (self.num_items - 1) + \
                               r"(.*)$"

                self.g = re.match(self.g_regex, s).groups() 

        def valid(self):
            if self.m:
                for sub_t in self.g:
                    if not PyType.valid(sub_t): return False
                return True
            else:
                return False

        def get_t(self):
            if self.m:
                return "tuple"

            # should not be called on invalid input.
            assert(False)

        def get_members(self):
            if self.m:
                return tuple(PytyType(sub_t) for sub_t in self.g)

            # should not be called on invalid input.
            assert(False)
            
    @staticmethod
    def kill_none_spots(tup):
        return tuple([t for t in tup if t is not None])

    def __init__(self, spec):
        kind = [k for k in type_grammar if k.matches(spec)]

        if len(kind) > 0:
            type_repr = kind[0](spec)

            if type_repr.valid():
                self.t = type_repr.get_t()
                self.members = type_repr.get_members()
            else:
                raise Exception("Invalid Pyty Type specificaiton!")
        else:
            raise Exception("Invalid Pyty Type specification!")

        """
        if PytyType.valid_type_string(spec):
            self.main_t = spec

            m = re.match(PytyType.type_regex, spec)

            self.members = []
            
            g = PytyType.kill_none_spots(m.groups())

            for i in range(0, len(g)):
                self.members.append(PytyType(g[i].strip()))
        else:
            raise Exception("Invalid Pyty Type specification.")
            """

    def is_base_type(self):
        return self.members is None

    def __eq__(self, other):
        return self.t == other.t and self.members == other.members

    def __repr__(self):
        if self.is_base_type():
            return self.t
        else:
            return self.t + ": " + str(self.members)

    def is_int(self):
        return self.t == "int"
    
    def is_float(self):
        return self.t == "float"

    def is_bool(self):
        return self.t == "bool"

    def is_subtype(self, other):
            
        return self.t == other.t or (self.is_int() and other.is_float())

        # XXX include more complicated rules for collection and function types

class PytyTypes:
    int_t = PytyType('int')
    float_t = PytyType('float')
    bool_t = PytyType('bool')


