#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from BedReader import BedReader
from BedGene import BedGene

#=========================================================================
# Attributes:
#   
# Instance Methods:
#   reader=BedGeneReader()
#   genes=reader.read(CDS_filename,UTR_filename=None)
# Class Methods:
#
# Private Methods:
#   genes=self.readCDS(filename)
#=========================================================================
class BedGeneReader:
    """BedGeneReader reads BedGene objects from a BED file"""
    def __init__(self):
        pass

    def read(CDS_filename,UTR_filename):
        genes=self.readCDS(CDS_filename)

    def readCDS(self,filename):
        reader=BedReader(filename)
        genes=[]
        genesByName={}
        while(True):
            record=reader.nextRecord()
            if(not record): break
            if(not record.isBed6()):
                raise Exception("BED file has too few fields")
            id=record.name
            gene=genesByName.get(id,None)
            if(not gene):
                gene=Gene(record.chr,record.strand)
                genesByName[id]=gene
                genes.append(gene)
        reader.close()
        return genes
