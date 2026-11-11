import os
import sys
from sage.all import *
from sage.doctest.control import DocTestController, DocTestDefaults
assert os.sched_getaffinity(0) == {1} and os.nice(0) >= 19
options = DocTestDefaults(long=True, serial=True, nthreads=1,
                          optional='sage', warn_long=120)
controller = DocTestController(options, ['upstream_doctests.py'])
sys.exit(controller.run())
