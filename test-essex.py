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
from EssexParser import EssexParser
import sys

BASE="/Users/bmajoros/python/test/data"
filename=BASE+"/HG00096-1-subset.essex"
parser=EssexParser(filename)
while(True):
    root=parser.nextElem()
    if(not root): break
    root.printXML(sys.stdout)
    print("\n")
