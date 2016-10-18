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
from FastaWriter import FastaWriter
from Interval import Interval

######################################################################
#
# FastbTrack.py bmajoros@duke.edu 10/14/2016
#
# A track in a Fastb file.
#
# Attributes:
#   type : "discrete" or "continuous"
#   id : name of track
#   data : string (for discrete) or array of float (for continuous)
#   deflineExtra : extra info for defline
# Methods:
#   track=FastbTrack(type,id,data,deflineExtra); # $type="discrete" or "continuous"
#   type=track.getType()
#   data=track.getData()
#   track.setSequence(string) # discrete
#   track.setData(values) # continuous
#   id=track.getID()
#   L=track.getLength()
#   track.rename(newID)
#   bool=track.isDiscrete()
#   bool=track.isContinuous()
#   track.save(FILEHANDLE)
#   array=track.getNonzeroRegions() # returns array of Interval
#   newTrack=track.slice(begin,end); # [begin,end) => end not inclusive
######################################################################

class FastbTrack:
    def __init__(self,type,id,data,deflineExtra):
        self.type=type
        self.id=id
        self.data=data
        self.deflineExtra=deflineExtra

    def getType(self):
        return self.type

    def getData(self):
        return self.data

    def isDiscrete(self):
        return self.type=="discrete"

    def isContinuous(self):
        return self.type=="continuous"

    def getID(self):
        return self.id

    def save(self,fh):
        writer=FastaWriter()
        id=self.id
        data=self.data
        deflineExtra=self.deflineExtra
        if(self.isDiscrete()):
            writer.addToFasta(">"+id+" "+deflineExtra,data,fh)
        else:
            fh.write("%"+id+" "+deflineExtra+"\n")
            n=len(data)
            for i in range(0,n): fh.write(str(data[i])+"\n")

    def getNonzeroRegions(self):
        """getNonzeroRegions() returns array of Intervals"""
        data=self.data
        if(self.isDiscrete()): raise Exception("track is not continuous")
        L=len(data)
        intervals=[]
        begin=None
        for i in range(0,L):
            x=data[i]
            if(x>0 and (i==0 or data[i-1]==0)): begin=i
            elif(x==0 and i>0 and data[i-1]>0):
                intervals.append(Interval(begin,i))
        if(L>0 and data[L-1]>0):
            intervals.append(Interval(begin,L))
        return intervals

    def rename(self,newID):
        self.id=newID

    def getLength(self):
        return len(self.data)

    def slice(self,begin,end):
        return FastbTrack(self.type,self.id,self.data[begin:end],
                          self.deflineExtra)

    def setSequence(self,string):
        self.data=string

    def setData(self,values):
        self.data=values
