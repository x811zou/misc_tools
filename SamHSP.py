#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from CigarString import CigarString
from Interval import Interval

#=========================================================================
# Attributes:
#   cigar : CigarString
#   refName : string
#   readInterval : Interval
#   refInterval : Interval
#   score : float
#   rec : the SamRecord this HSP came from
# Instance Methods:
#   hsp=SamHSP(rec,cigar) # rec is a SamRecord
#   cigar=hsp.getCigar() # returns CigarString object
#   refName=hsp.getRefName()
#   boolean=hsp.overlapsOnRead(otherHSP)
#   boolean=hsp.overlapsOnRef(otherHSP)
#   interval=hsp.getReadInterval()  # returns Interval object
#   interval=hsp.getRefInterval() # returns Interval object
#   hsp.computeScore()
#   score=hsp.getScore()
#   str=hsp.toString()
# Private Methods:
#   self.computeIntervals()
# Class Methods:
#   none
#=========================================================================
class SamHSP:
    """SamHSP"""
    def __init__(self,rec,cigar):
        self.cigar=cigar
        self.refName=rec.getRefName()
        self.rec=rec
        self.computeIntervals()
        self.score=None

    def toString(self):
        return self.refName+"|"+self.cigar.toString()+"|"+\
            self.readInterval.toString()+"|"+str(self.score)

    def getScore(self):
        return self.score

    def computeScore(self):
        mismatches=self.rec.countMismatches()
        matches=self.cigar.totalAlignmentLength()-mismatches
        indelBases=self.cigar.countIndelBases()
        numerator=matches
        denominator=1+mismatches+indelBases
        self.score=float(numerator)/float(denominator)

    def overlapsOnRead(self,other):
        return self.readInterval.overlaps(other.readInterval)

    def overlapsOnRef(self,other):
        return self.refInterval.overlaps(other.refInterval)

    def getCigar(self):
        return self.cigar

    def getRefName(self):
        return self.refName

    def getReadInterval(self):
        return self.readInterval

    def getRefInterval(self):
        return self.refInterval

    def computeIntervals(self):
        cigar=self.cigar
        n=cigar.length()
        firstOp=cigar[0]
        lastOp=cigar[n-1]
        self.readInterval=Interval(firstOp.getQueryInterval().getBegin(),
                                   lastOp.getQueryInterval().getEnd())
        self.refInterval=Interval(firstOp.getRefInterval().getBegin(),
                                  lastOp.getRefInterval().getEnd())
            


