spec mode: expr
expr type: Tuple

----pass----
(1,2,3) : (int, int, int)
(1,) : (int,)
(True,) : (bool,)
(True, False) : (bool, bool)
(1.0, 2.0) : (float, float)
(-1.0, 4.5) : (float, float)
(True, 4, -3.0, True) : (bool, int, float, bool)
((True, False), (True,)) : ((bool, bool), (bool,))
([1,2,3,4,5], [1.0,2.0,3.0], [True, False]) : ([int], [float], [bool])

----fail----
(True, 4, 3.0) : (bool, float, float) # SUBTYPING
(1,) : (int)
(4.0, 3) : (int, int)
(True,) : (int,)
((5,4), 3) : (int, int)
([1, 2, 3], [True, False]) : (int, bool)
(1, 2, 3) : (int)
(1, 2, 3) : (int, int)
(1, 2, 3) : (int, int, int, int)
(1, 2, 3) : (int, int, int, int, int)
(1, 2, 3, 4, 5) : (int, int, int)
(1, 2, 3, 4, 5) : (int, int, int, int)

----TypeIncorrectlySpecifiedError----
((True,), 5) : ((,))
