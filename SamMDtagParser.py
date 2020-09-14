#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)

#=========================================================================
# Attributes:
#   
# Instance Methods:
#   SamMDtagParser()
# Class Methods:
#   N=SamMDtagParser.countMismatches(MDtags)
#=========================================================================
class SamMDtagParser:
    """SamMDtagParser"""
    def __init__(self):
        pass

    @classmethod
    def countMismatches(cls,MDtags):
        mismatches=0
        L=len(MDtags)
        for i in range(L):
            if(i%2==1):
                if(len(MDtags[i])==1): mismatches+=1
        return mismatches



