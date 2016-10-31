#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from Rex import Rex

#=========================================================================
# Attributes:
#   
# Instance Methods:
#   reader=GFF3Parser()
#   transcriptArray=reader.loadGFF(filename)
#   geneList=reader.loadGenes(filename)
#   hashTable=reader.hashBySubstrate(filename)
#   hashTable=reader.hashGenesBySubstrate(filename)
#   hashTable=reader.loadTranscriptIdHash(filename)
#   hashTable=reader.loadGeneIdHash(filename)
#
# Private Methods:
#   structure=parser.loadStructure(filename)
#   records=parser.loadRecord(filename)
#   record=self.parseRecord(fields)
#=========================================================================
class GFF3Parser:
    """GFF3Parser"""
    def __init__(self):
        pass

    def loadStructure(self,filename):
        records=self.loadRecords(filename)
        idHash={}
        self.hashRecordsByID(records,idHash)
        self.connectParentsChildren(records,idHash)
        roots=self.findRoots(records)
        for root in roots:
            print(root["type"])
            
    def findRoots(self,records):
        roots=[]
        for record in records:
            if(record.get("children",None) is not None):
                roots.append(record)
        return roots

    def addChild(self,parent,child):
        if(parent.get("children",None) is None): parent["children"]=[]
        parent["children"].append(child)
        child["parent"]=parent
        
    def connectParentsChildren(self,records,idHash):
        for record in records:
            parent=record["extra"].get("Parent",None)
            if(parent is not None):
                parentRec=idHash.get(parent,None)
                if(parentRec is None):
                    raise Exception("Cannot find GFF3 parent "+parent)
                self.addChild(parentRec,record)

    def hashRecordsByID(self,records,hash):
        for record in records:
            extraHash=record["extra"]
            ID=extraHash.get("ID",None)
            if(ID is not None): hash[ID]=record
    
    def loadRecords(self,filename):
        fh=open(filename,"rt")
        records=[]
        while(True):
            line=fh.readline()
            if(line==""): break
            fields=line.split(sep="\t")
            numFields=len(fields)
            if(numFields<9): continue
            rec=self.parseRecord(fields)
            records.append(rec)
        fh.close()
        return records

    def parseRecord(self,fields):
        if(len(fields)>9):
            raise Exception("too many fields in GFF3 record"+"\t".join(fields))
        (substrate,source,type,begin,end,score,strand,frame,extra)=fields
        extra=extra.rstrip()
        extraFields=extra.split(";")
        extraHash={}
        rex=Rex()
        for field in extraFields:
            if(not rex.find("(.+)=(.+)",field)):
                raise Exception("Can't parse GFF3 field: "+field)
            extraHash[rex[1]]=rex[2]
        rec={"substrate":substrate,
             "source":source,
             "type":type,
             "begin":begin,
             "end":end,
             "score":score,
             "strand":strand,
             "frame":frame,
             "extra":extraHash}
        return rec
        
def test_parser(filename):
    parser=GFF3Parser()
    records=parser.loadStructure(filename)

test_parser("/Users/bmajoros/python/test/data/subset.gff3")

