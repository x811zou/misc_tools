#!/bin/env python
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii, chr, 
   hex, input, next, oct, open, pow, round, super, filter, map, zip)
import ProgramName
import sys
from Interval import Interval

# Process command line
name=ProgramName.get();
if(len(sys.argv)!=3):
  print(name," <parm1> <parm2>")
  exit()
parm1=sys.argv[1]
parm2=sys.argv[2]
print(parm1, parm2)

print ("Hello, world\n")

for i in range(1,10):
  print (i,end="")
print("\n")

i1=Interval(1,6)
i2=Interval(4,9)
u=i1.union(i2)
print(u)
print(i1)




