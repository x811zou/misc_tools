#!/bin/env python
#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from Fastb import Fastb
import ProgramName
import sys

if(len(sys.argv)!=2):
    sys.exit(ProgramName.get()+" in.fastb")
filename=sys.argv[1]

fastb=Fastb(filename)
numTracks=fastb.numTracks()
for i in range(numTracks):
    track=fastb.getIthTrack(i)
    L=track.getLength()
    id=track.getID()
    print(id+"\t"+str(L))
