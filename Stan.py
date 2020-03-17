#!/usr/bin/env python
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
import os

######################################################################
# Attributes:
#    
# Methods:
#    stan=Stan(model)
#    stan.run(numWarmup,numSamples,inputFile,outputFile,stderrFile,initFile=None):
#    stan.writeOneDimArray(name,array,dim,OUT):
#    stan.writeTwoDimArray(name,array,firstDim,secondDim,OUT):
#    stan.writeThreeDimArray(name,array,firstDim,secondDim,thirdDim,OUT):
#    stan.initArray2D(dim1,dim2,value):
#    stan.initArray3D(dim1,dim2,dim3,value):

######################################################################

class Stan:
    def __init__(self,model):
        self.model=model

    def writeOneDimArray(self,name,array,dim,OUT):
        print(name+" <- c(",end="",file=OUT)
        for i in range(0,dim):
            print(array[i],end="",file=OUT)
            if(i+1<dim): print(",",end="",file=OUT)
        print(")",file=OUT)

    def writeTwoDimArray(self,name,array,firstDim,secondDim,OUT):
        print(name+" <- structure(c(",end="",file=OUT)
        for j in range(secondDim): # second dim
            for i in range(firstDim): # first dim
                print(array[i][j],end="",file=OUT)
                if(i+1<firstDim): print(",",end="",file=OUT)
            if(j+1<secondDim): print(",",end="",file=OUT)
        print("), .Dim=c(",firstDim,",",secondDim,"))",sep="",file=OUT)

    def writeThreeDimArray(self,name,array,firstDim,secondDim,thirdDim,OUT):
        print(name+" <- structure(c(",end="",file=OUT)
        for k in range(thirdDim): # third dim
            for j in range(secondDim): # second dim
                for i in range(firstDim): # first dim
                    print(array[i][j][k],end="",file=OUT)
                    if(i+1<firstDim): print(",",end="",file=OUT)
                if(j+1<secondDim): print(",",end="",file=OUT)
            if(k+1<thirdDim): print(",",end="",file=OUT)
        print("), .Dim=c(",firstDim,",",secondDim,",",thirdDim,"))",sep="",file=OUT)

    def initArray2D(self,dim1,dim2,value):
        array=[]
        for i in range(dim1):
            row=[]
            for j in range(dim2):
                row.append(value)
            array.append(row)
        return array

    def initArray3D(self,dim1,dim2,dim3,value):
        array=[]
        for i in range(dim1):
            row=[]
            for j in range(dim2):
                row2=[]
                for k in range(dim3):
                    row2.append(value)
                row.append(row2)
            array.append(row)
        return array

    def run(self,numWarmup,numSamples,inputFile,outputFile,stderrFile,initFile=None):
        cmd=self.getCmd(numWarmup,numSamples,inputFile,outputFile,stderrFile,initFile)
        os.system(cmd)

    def getCmd(self,numWarmup,numSamples,inputFile,outputFile,stderrFile,initFile=None):
        init=" init="+initFile if initFile is not None else ""
        cmd=self.model+" sample thin=1"+\
            " num_samples="+str(numSamples)+\
            " num_warmup="+str(numWarmup)+\
            " data file="+inputFile+\
            init+\
            " output file="+outputFile+" refresh=0 > "+stderrFile
        return cmd
        
