#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
import random

#=========================================================================
# Attributes:
#   
# Instance Methods:
#   Shuffler()
# Class Methods:
#   
#=========================================================================
class Shuffler:
    """Shuffler shuffles arrays and strings"""
    def __init__(self):
        pass

    @classmethod
    def shuffleArray(cls,array):
        L=len(array)
        for i in range(L):
            j=random.randint(0,L-1)
            temp=array[i]
            array[i]=array[j]
            array[j]=temp

    @classmethod
    def shuffleString(cls,string):
        L=len(string)
        ret=string
        for i in range(L):
            j=random.randint(0,L-1)
            if(j==i): continue
            if(j>i):
                ret=ret[0:i]+ret[j]+ret[i+1:j]+ret[i]+ret[j+1:L]
            else:
                ret=ret[0:j]+ret[i]+ret[j+1:i]+ret[j]+ret[i+1:L]
        return ret
