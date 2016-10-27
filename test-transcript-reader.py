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
from GffTranscriptReader import GffTranscriptReader

#filename="/home/bmajoros/1000G/assembly/local-genes.gff"
#filename="/home/bmajoros/1000G/assembly/tmp.gff"
#filename="test/data/tmp.gff"
filename="test/data/local-genes.gff"

reader=GffTranscriptReader()
#transcripts=reader.loadGFF(filename)
#for transcript in transcripts:
    #print(transcript.getID())
    #gff=transcript.toGff()
    #print(gff)
   
#genes=reader.loadGenes(filename)
#for gene in genes:
#    print("gene",gene.getID())
#    n=gene.getNumTranscripts()
#    for i in range(n):
#        transcript=gene.getIthTranscript(i)
#        transID=transcript.getID()
#        print("\t"+transID+"\t"+str(transcript.getBegin())+"\t"
#              +str(transcript.getEnd()))

#hashTable=reader.hashBySubstrate(filename)
#keys=hashTable.keys()
#for key in keys:
#    print(key)

#hashTable=reader.hashGenesBySubstrate(filename)
#keys=hashTable.keys()
#for key in keys:
#    print(key)

#hashTable=reader.loadTranscriptIdHash(filename)
#keys=hashTable.keys()
#for key in keys:
#    print(key)

hashTable=reader.loadGeneIdHash(filename)
keys=hashTable.keys()
for key in keys:
    print(key)

