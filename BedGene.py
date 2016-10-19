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
#   chr : string (chromosome name)
#   strand : string ("+" or "-", or "." if unknown)
#   CDS : array of Interval
#   UTR : array of Interval
#   exons : array of Interval : includes both CDS and UTR
# Instance Methods:
#   gene=BedGene(chr,strand)
#   gene.addCDS(Interval(begin,end))
#   gene.addUTR(Interval(begin,end))
#   gene.addExon(Interval(begin,end))
#   gene.coalesce() # combines UTR and CDS elements into exons
# Class Methods:
#=========================================================================
class BedGene:
    """BedGene"""
    def __init__(self,chr,strand):
        self.exons=[]
        self.chr=chr
        self.strand=strand

    def addCDS(self,interval):
        self.CDS.append(interval)

    def addUTR(self,interval):
        self.UTR.append(interval)

    def addExon(self,interval):
        self.exons.append(interval)

    def coalesce(self):
        exons=self.exons=[]
        for cds in self.CDS: exons.append(cds.clone())
        for utr in self.UTR:
            added=False
            for exon in exons:
                if(utr.begin<exon.begin and utr.end>=exon.begin):
                    exon.begin=utr.begin
                    added=True
                    break
                elif(utr.end>exon.end and utr.begin<=exon.end):
                    exon.end=utr.end
                    added=True
                    break
            if(not added): exons.append(utr)
