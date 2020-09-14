#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)

#=========================================================================
# Attributes:
#   
# Instance Methods:
#   clusterer=SamHspClusterer()
# Class Methods:
#   clustered=SamHspClusterer.cluster(HSPs)
#=========================================================================
class SamHspClusterer:
    """SamHspClusterer"""
    def __init__(self):
        pass

    @classmethod
    def cluster(cls,raw):
        HSPs=[x for x in raw]
        HSPs.sort(key=lambda hsp: hsp.getReadInterval().getBegin())
        for hsp in HSPs: hsp.computeScore()
        n=len(HSPs)
        i=0
        while(i<n-1):
            while(HSPs[i].overlapsOnRead(HSPs[i+1])):
                if(HSPs[i].getScore()<HSPs[i+1].getScore()):
                    del HSPs[i]
                else:
                    del HSPs[i+1]
                n-=1
                if(i>=n-1): break
            i+=1
        return HSPs

