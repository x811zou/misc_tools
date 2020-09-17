#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from SamHSP import SamHSP

#=========================================================================
# Attributes:
#   HSPs : array of SamHSP
# Instance Methods:
#   anno=SamAnnotation(HSPs) # makes shallow copy of array elements
#   n=anno.numHSPs()
#   HSPs=anno.getHSPs()
#   boolean=anno.allRefsSame() # are all references the same?
#   refName=anno.firstRef() # returns reference name of first HSP
#   refNames=anno.getRefNames() # returns all reference names as a set
#   n=anno.numDifferentRefs() # returns number of different refs among HSPs
#   array=anno.getReadGaps(includeMargins=True)
#   array=anno.getReadGapLengths(includeMargins=True)
#   array=anno.getRefGaps()
#   array=anno.getRefGapLengths()
#   L=anno.getReadLength() # returns length of entire read (not just HSP)
# Class Methods:
#   none
#=========================================================================
class SamAnnotation:
    """SamAnnotation"""
    def __init__(self,HSPs):
        self.HSPs=[]
        for hsp in HSPs:
            self.HSPs.append(hsp)

    def getReadLength(self):
        HSPs=self.HSPs
        n=len(HSPs)
        if(n==0): raise Exception("Don't know read length: no HSPs")
        return HSPs[0].getRec().seqLength()

    def getReadGaps(self,includeMargins=True):
        L=self.getReadLength()
        HSPs=self.HSPs
        numHSPs=len(HSPs)
        if(numHSPs==0): return Interval(0,L)
        intervals=[]
        if(includeMargins):
            b=HSPs[0].getReadInterval().getBegin()
            if(b>0): intervals.append(Interval(0,b))
        for i in range(numHSPs-1):
            b=HSPs[i].getReadInterval().getEnd()
            e=HSPs[i+1].getReadInterval().getBegin()
            if(b<e): intervals.append(Interval(b,e))
        if(includeMargins):
            e=HSPs[numHSPs-1].getReadInterval().getEnd()
            if(e<L):
                intervals.append(Interval(e,L))
        return intervals

    def getRefGaps(self):
        HSPs=self.HSPs
        numHSPs=len(HSPs)
        if(numHSPs==0): return []
        intervals=[]
        if(includeMargins):
            b=HSPs[0].getRefInterval().getBegin()
            if(b>0): intervals.append(Interval(0,b))
        for i in range(numHSPs-1):
            b=HSPs[i].getRefInterval().getEnd()
            e=HSPs[i+1].getRefInterval().getBegin()
            if(b<e): intervals.append(Interval(b,e))
        if(includeMargins):
            e=HSPs[numHSPs-1].getRefInterval().getEnd()
            if(e<L):
                intervals.append(Interval(e,L))
        return intervals

    def getReadGapLengths(self,includeMargins=True):
        intervals=self.getReadGaps(includeMargins)
        lengths=[x.getLength() for x in intervals]
        return lengths

    def getRefGapLengths(self):
        intervals=self.getRefGaps()
        lengths=[x.getLength() for x in intervals]
        return lengths
            
    def numDifferentRefs(self):
        names=self.getRefNames()
        return len(names)

    def getRefNames(self):
        names=set()
        for hsp in self.HSPs:
            set.add(hsp.getRefName())
        return names

    def firstRef(self):
        HSPs=self.HSPs
        n=len(HSPs)
        if(n==0): raise Exception("HSPs is empty in SamAnnotation")
        return HSPs[0].getRefName()

    def numHSPs(self):
        return len(self.HSPs)

    def getHSPs(self):
        return self.HSPs

    def allRefsSame(self):
        HSPs=self.HSPs
        n=len(HSPs)
        if(n==0): return True
        ref=HSPs[0].getRefName()
        for i in range(1,n):
            if(HSPs[i].getRefName()!=ref):
                return False
        return True


