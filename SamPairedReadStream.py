#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from SamReader import SamReader
from SamPairedRead import SamPairedRead

#=========================================================================
# Attributes:
#   reader : SamReader
#   dedup : boolean
#   buffer : SamRecord
# Instance Methods:
#   stream=SamPairedReadStream(filename,dedup=True)
#   pair=stream.nextPair() # returns SamPairedRead
# Class Methods:
#   none
#=========================================================================
class SamPairedReadStream:
    """SamPairedReadStream"""
    def __init__(self,filename,dedup=True):
        self.reader=SamReader(filename)
        self.dedup=dedup
        self.buffer=None

    def nextPair(self):
        while(True):
            rec=None
            if(self.buffer is not None): 
                rec=self.buffer
                self.buffer=None
            else: rec=self.reader.nextSequence()
            if(rec is None): return None
            if(rec.flag_unmapped()): continue
            if(self.dedup and rec.flag_PCRduplicate()): continue
            if(not rec.flag_firstOfPair()): continue
            read1=rec
            rec=self.reader.nextSequence()
            if(rec is None): return None
            if(rec.flag_unmapped()): continue
            if(self.dedup and rec.flag_PCRduplicate()): continue
            if(rec.flag_firstOfPair()): 
                self.buffer=rec
                continue
            read2=rec
            return SamPairedRead(read1,read2)





