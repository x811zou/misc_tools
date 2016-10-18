#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from Bed3Record import Bed3Record

#=========================================================================
# Inherited Attributes:
#   chr : string
#   interval : Interval
# Attributes:
#   name : string
#   score : float
#   strand : string
# Instance Methods:
#   record=Bed6Record(chr,begin,end,name,score,strand)
#   bool=isBed3()
#   bool=isBed6()
# Class Methods:
#   
#=========================================================================
class Bed6Record(Bed3Record):
    """Bed6Record represents a record in a BED6 file"""
    def __init__(self,chr,begin,end,name,score,strand):
        Bed3Record.__init__(self,chr,begin,end)
        self.name=name
        self.score=score
        self.strand=strand

    def isBed3(self):
        return False

    def isBed6(self):
        return True


