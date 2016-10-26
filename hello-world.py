#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii, chr, 
   hex, input, next, oct, open, pow, round, super, filter, map, zip)
import ProgramName
import sys
import os
from Interval import Interval
from ConfigFile import ConfigFile
from SummaryStats import SummaryStats
import random

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

#import tempfile
#[fh,filename]=tempfile.mkstemp(prefix="tmp.");
#print(filename,fh)
#os.close(fh)

import TempFilename
filename=TempFilename.generate()
fh=open(filename,'w')
print(fh)
x=0
while(x<10):  fh.write(str(x)); x+=3
fh.close()
os.remove(filename)

config=ConfigFile("test/data/ice.0-43.config")
print(config.lookup("donor-consensus"))

a=[1.1, 6.4, 9.3, 3.4, 9.2, 4.6, 1.6, 0.3]
b=list(map(lambda x:x+random.uniform(-10,10),a))
[mean,SD,min,max]=SummaryStats.summaryStats(a)
print(mean,"+/-",SD)
print("sum=",SummaryStats.sum(a))
print("r=",SummaryStats.correlation(a,b))



