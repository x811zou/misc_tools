#!/usr/bin/env python
import sys
import os
import gzip

if(len(sys.argv)!=2):
   print sys.argv[0]+" <in.vcf.gz>"
   sys.exit(0)
[infile]=sys.argv[1:]

for line in gzip.open(infile):
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
      print id+":chr"+chr+":"+pos+":"+ref+":"+alt+"\t",
      genotypes=fields[9:]
      for i in range(0,numIndiv):
         id=individuals[i]
         gt=genotypes[i]
         genotype[id].append(gt)
print "\n"
for id in individuals:
   gt=genotype[id]
   print id+"\t"+"\t".join(gt)
