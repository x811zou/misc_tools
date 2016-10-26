#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
import re

#=========================================================================
# Attributes:
#   match : returned from re.search()
# Instance Methods:
#   r=RegEx()
#   bool=r.find("abc(\d+)def(\d+)ghi(\d+)",line)
#   x=r[1]; y=r[2]; z=r[3]
#=========================================================================
class RegEx:
    """RegEx -- more compact regular expression matching similar to Perl"""

    def __init__(self):
        match=None

    def find(self,pattern,line):
        self.match=re.match(pattern,line)
        return self.match is not None

    def __getitem__(self,index):
        return self.match.group(index)

def test_regex():
    rex=RegEx()
    x=y=z=None
    if(rex.find("abc(\d+)abc(\d+)abc","ab123abc456abc789")):
        x=rex[1]; y=rex[2]
    elif(rex.find("dog(\d+)cat(\d+)cow(\d+)chicken(\d+)",
                  "dog1cat2cow8chicken100")):
        x=rex[1]; y=rex[4]
    print(x,y)



