
# This setup.py will compile and install the subsets extension
# Use:
#    setup.py install
#
# In Python 2.2 the extension is copied into
# <pythonhome>/lib/site-packages
# in earlier versions it may be put directly in the python directory.

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import Cython.Compiler.Options
Cython.Compiler.Options.embed_pos_in_docstring = True
import numpy
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

print numpy_include


setup(name = "dna2int",
       version = "1.0",
       maintainer = "",
       maintainer_email = "",
       description = "",
       cmdclass = {'build_ext': build_ext},

       ext_modules = [
              
    Extension("dna2int", ["dna2int.pyx"]),
        ]
)
# end of file: setup.py

