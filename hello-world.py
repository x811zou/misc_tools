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

i1=Interval(1,10)
i2=Interval(1.5,7.3)
sub=i1.minus(i2)
print(sub)

a=["a","b","c"]
for x in a:
   print(x)

def main():
   try:
      raise Exception("cookie")
   except Exception as e:
      print(e)

main()

my_generator = (letter for letter in 'abcdefg')

x=0
while(x<10):  print(x); x+=3


