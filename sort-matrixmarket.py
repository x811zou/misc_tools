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
import gzip
from Pipe import Pipe
import TempFilename

HEADERFILE=TempFilename.generate(".header")
SORTEDFILE=TempFilename.generate(".sorted")

#=========================================================================
# main()
#=========================================================================
if(len(sys.argv)!=4):
    exit(ProgramName.get()+" in.mtx.gz column out.mtx.gz\n    where column = 1-based field index\n")
(infile,index,outfile)=sys.argv[1:]

OUT=open(HEADERFILE,"wt")
numHeader=1
with gzip.open(infile,"rt") as IN:
    for line in IN:
        if(len(line)==0): raise Exception("unexpected empty line")
        if(line[0]=="%"): 
            numHeader+=1
            print(line,file=OUT,end="")
        else: 
            print(line,file=OUT,end="")
            break
IN.close(); OUT.close()

cmd="cat "+infile+" | gunzip | tail -n +"+str(numHeader+1)+\
    " | sort -g -k "+index+" > "+SORTEDFILE
print(cmd) ###
Pipe.run(cmd)
cmd="cat "+HEADERFILE+" "+SORTEDFILE+" | gzip > "+outfile
print(cmd) ###
Pipe.run(cmd)
Pipe.run("rm "+SORTEDFILE)
Pipe.run("rm "+HEADERFILE)
