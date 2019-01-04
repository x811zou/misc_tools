#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# 2018 William H. Majoros (bmajoros@alumni.duke.edu)
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)

#=========================================================================
# Attributes:
#   op : M/I/D/S
#   length : integer
# Instance Methods:
#   op=CigarOp("M",135)
#=========================================================================
class CigarOp:
    def __init__(self,op,L):
        self.op=op
        self.length=L

