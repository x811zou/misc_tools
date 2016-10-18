#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from Bed3Record import Bed3Record
from Bed6Record import Bed6Record
import re

#=========================================================================
# Attributes:
#   fh : file handle
# Instance Methods:
#   reader=BedReader(filename)
#   reader.close()
#   record=reader.nextRecord() # Bed3Record or Bed6Record
# Class Methods:
#   
#=========================================================================
class BedReader:
    """BedReader reads bed3 and/or bed6 files"""
    def __init__(self,filename):
        self.fh=open(filename,"r")

    def close(self):
        self.fh.close()

    def nextRecord(self):
        while(True):
            line=self.fh.readline()
            if(not line): return None
            if(not re.search("\S",line)): continue
            line=line.rstrip()
            line=line.lstrip()
            fields=line.split()
            n=len(fields)
            if(n==3):
                return Bed3Record(fields[0],int(fields[1]),int(fields[2]))
            if(n==4):
                return Bed6Record(fields[0],int(fields[1]),int(fields[2]),
                                  fields[3],0.0,".")
            if(n==5):
                return Bed6Record(fields[0],int(fields[1]),int(fields[2]),
                                  fields[3],float(fields[4]),".")
            if(n==6):
                return Bed6Record(fields[0],int(fields[1]),int(fields[2]),
                                  fields[3],float(fields[4]),fields[5])
            raise Exception("wrong number of fields in bed file: "+line)

