#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from Interval import Interval

#=========================================================================
# Attributes:
#   chr : string
#   interval : Interval
# Instance Methods:
#   record=Bed3Record(chr,begin,end)
#   bool=record.isBed3()
#   bool=record.isBed6()
#   begin=record.getBegin()
#   end=record.getEnd()
# Class Methods:
#   
#=========================================================================
class Bed3Record:
    """Bed3Record represents a record in a BED3 file"""
    def __init__(self,chr,begin,end):
        self.chr=chr
        self.interval=Interval(begin,end)

    def isBed3(self):
        return True

    def isBed6(self):
        return False

    def getBegin(self):
        return self.interval.begin

    def getEnd(self):
        return self.interval.end