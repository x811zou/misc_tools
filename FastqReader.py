#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# 2018 William H. Majoros (bmajoros@allumni.duke.edu)
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from Rex import Rex
rex=Rex()
import gzip

#=========================================================================
# Attributes:
#   fh : file handle
# Instance Methods:
#   reader=FastqReader(filename)
#   (ID,seq,qual,pair)=reader.nextSequence() # returns None at EOF
#   reader.close()
# Class Methods:
#=========================================================================
class FastqReader:
    """FastqReader"""
    def __init__(self,filename):
        if(filename is not None):
            if(rex.find("\.gz$",filename)): self.fh=gzip.open(filename,"rt")
            else: self.fh=open(filename,"r")

    def close(self):
        self.fh.close()

    def nextSequence(self):
        fh=self.fh
        line=fh.readline()
        if(line is None): return None
        if(len(line)==0): return None
        if(not rex.find("^(\S+)",line)):
            return None
            #raise Exception("Cannot parse fastq line: "+ID)
        ID=rex[1]
        pair=1
        if(rex.find("\s+(\d)",line)): pair=int(rex[1])
        seq=fh.readline().rstrip()
        junk=fh.readline()
        qual=fh.readline().rstrip()
        return (ID,seq,qual,pair)
        


