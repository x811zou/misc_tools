#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# 2018 William H. Majoros (bmajoros@alumni.duke.edu)
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from Rex import Rex
rex=Rex()
from CigarOp import CigarOp

#=========================================================================
# Attributes:
#   ops : array of CigarOp
# Instance Methods:
#   cigar=CigarString(string)
#   bool=cigar.completeMatch()
#   numOps=cigar.length()
#   cigarOp=cigar[i] # returns a CigarOp object
#=========================================================================
class CigarString:
    """CigarString parses CIGAR strings (alignments)"""
    def __init__(self,cigar):
        self.ops=self.parse(cigar)

    def length(self):
        return len(self.ops)

    def __getitem__(self,i):
        return self.ops[i]
        
    def completeMatch(self):
        ops=self.ops
        return len(ops)==1 and ops[0].op=="M"

    def toString(self):
        ops=self.ops
        s=""
        for op in ops:
            s+=str(op.length)
            s+=op.op
        return s

    def parse(self,cigar):
        array=[]
        if(cigar=="*"): return array
        while(len(cigar)>0):
            if(not rex.find("(\d+)(.)",cigar)):
                raise Exception("Can't parse CIGAR string: "+cigar)
            L=int(rex[1])
            op=rex[2]
            rec=CigarOp(op,L)
            array.append(rec)
            rex.find("\d+.(.*)",cigar)
            cigar=rex[1]
        return array

