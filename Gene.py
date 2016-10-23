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
# The above imports should allow this program to run in both Python 2 and
# Python 3.  You might need to update your version of module "future".

######################################################################
# Attributes:
#   transcripts : list of Transcript objects
#   ID
#   transcriptHash : transcripts hashed by their ID
# Methods:
#   gene=Gene()
#   gene.addTranscript(t)
#   n=gene.getNumTranscripts()
#   t=gene.getIthTranscript(i)
#   t=gene.longestTranscript()
#   id=gene.getId()
#   gene.setId(id)
#   begin=gene.getBegin() # leftmost edge
#   end=gene.getEnd()     # rightmost edge
#   strand=gene.getStrand()
#   substrate=gene.getSubstrate()
#   gff=gene.toGff()
#   
######################################################################

class Gene:
    def __init__(self):
        self.transcripts=[]
        self.transcriptHash={}

    def getStrand(self):
        transcripts=self.transcripts
        transcript=transcripts[0]
        return transcript.getStrand()

    def getSubstrate(self):
        transcripts=self.transcripts
        transcript=transcripts[0]
        return transcript.getSubstrate()

    def getBegin(self):
        transcripts=self.transcripts
        begin=None
        for transcript in transcripts:
            b=transcript.getBegin()
            if(begin is None or b<begin): begin=b
        return begin

    def getEnd(self):
        transcripts=self.transcripts
        end=None
        for transcript in transcripts:
            e=transcript.getEnd()
            if(end is None or e>end): end=e
        return end

    def addTranscript(self,transcript):
        id=transcript.getTranscriptId()
        hash=self.transcriptHash
        if(hash.get(id,None) is not None): return
        self.transcripts.append(transcript)
        hash[id]=transcript

    def getNumTranscripts(self):
        return len(self.transcripts)

    def getIthTranscript(self,i):
        return self.transcripts[i]

    def longestTranscript(self):
        transcripts=self.transcripts
        if(len(transcripts)==0): return None
        longest=transcripts[0]
        longestLength=longest.getExtent()
        for transcript in transcripts[1:]:
            length=transcript.getExtent()
            if(length>longestLength):
                longest=transcript
                longestLength=length
        return longest

    def getId(self):
        return self.ID

    def setId(self,id):
        self.ID=id

    def getBeginAndEnd(self):
        transcripts=self.transcripts
        begin=None
        end=None
        for transcript in transcripts:
            b=transcript.getBegin()
            e=transcript.getEnd()
            if(begin is None): begin=b; end=e
            else:
                if(b<begin): begin=b
                if(e>end): end=e
        return (begin,end)

    def toGff(self):
        transcripts=self.transcripts
        gff=""
        for transcript in transcripts:
            gff+=transcript.toGff()
        return gff

    def __hash__(self):
        return hash(self.ID)

    def __eq__(self,other):
        return self.ID==other.ID

    
