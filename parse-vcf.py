#!/usr/bin/env python
#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Author: William H. Majoros (bmajoros@alumni.duke.edu)
#=========================================================================
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
# The above imports should allow this program to run in both Python 2 and
# Python 3.  You might need to update your version of module "future".
import sys
import os
import gzip

if(len(sys.argv)!=3):
   print(sys.argv[0]+" <in.vcf.gz> <indiv>")
   sys.exit(0)
(infile,indiv)=sys.argv[1:]

numIndiv=None
with gzip.open(infile,"rt") as IN:
   for line in IN:
      line.rstrip("\n")
      fields=line.split()
      if len(fields)<7: continue
      if fields[0]=="#CHROM":
         individuals=fields[9:]
         numIndiv=len(individuals)
         genotype={}
         for id in individuals: genotype[id]=[]
      elif fields[6]=="PASS":
         [chr,pos,id,ref,alt]=fields[:5]
         #print(id+":chr"+chr+":"+pos+":"+ref+":"+alt+"\t")
         genotypes=fields[9:]
         for i in range(0,numIndiv):
            id=individuals[i]
            gt=genotypes[i]
            genotype[id].append(gt)
print("\n")
for id in individuals:
   gt=genotype[id]
   print(id+"\t"+"\t".join(gt))

