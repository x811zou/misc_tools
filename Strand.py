#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from enum import Enum

#=========================================================================
# Attributes:
#   FORWARD : int
#   REVERSE : int
# Instance Methods:
#   Strand()
# Class Methods:
#   toString(Strand)
#=========================================================================
class Strand(Enum):
    FORWARD=1
    REVERSE=0
        
    @classmethod
    def toString(cls,strand):
        return "+" if strand==strand.FORWARD else "-"




