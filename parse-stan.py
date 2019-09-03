#!/usr/bin/env python
#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Author: William H. Majoros (bmajoros@alumni.duke.edu)
#=========================================================================
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
# The above imports should allow this program to run in both Python 2 and
# Python 3.  You might need to update your version of module "future".
import sys
import ProgramName
from StanParser import StanParser

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)<3):
    exit(ProgramName.get()+" <infile.txt> <var1> <var2> ...\n")
infile=sys.argv[1]
variables=sys.argv[2:]

parser=StanParser(infile)
#(median,mean,SD,min,max)=parser.getSummary(variable)
#print("# posterior median=",median,sep="")
samplesByVar=[]
n=0
for var in variables:
    samples=parser.getVariable(var)
    samplesByVar.append(samples)
    n=len(samples)
for i in range(n):
    line=[]
    for sample in samplesByVar: line.append(str(sample[i]))
    print("\t".join(line))
         


