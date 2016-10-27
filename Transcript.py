#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
from Exon import Exon
from Translation import Translation
from CodonIterator import CodonIterator
import copy

######################################################################
# bmajoros@duke.com 10/15/2016
#
# Attributes:
#   substrate : scaffold or chromosome name
#   source : name of entity that predicted or curated this transcript
#   startCodon : index into (spliced) transcript sequence of ATG,
#                regardless of strand
#   startCodonAbsolute : absolute coordinates of start codon, 
#                        relative to genomic axis
#   strand : + or -
#   exons : pointer to array of Exons (which are actually CDS segments)
#   UTR : pointer to array of UTR segments
#   rawExons : point to array of exons (could be mix of CDS & UTR)
#   begin : begin coordinate of leftmost exon (zero based)
#   end : end coordinate of rightmost exon (one past end)
#   sequence : NOT LOADED BY DEFAULT!
#   transcriptId : identifier
#   stopCodons : hash table of stop codons (strings)
#   geneId : identifier of gene to which this transcript belongs
#   gene : a Gene object to which this transcript belongs
#   extraFields : a string of extra fields from the end of the GFF line
# Methods:
#   transcript=Transcript(id,strand)
#   transcript=Transcript(essexNode);
#   rawExons=transcript.getRawExons() # includes UTR (possibly coalesced)
#   transcript.addExon(exon)
#   copy=transcript.copy()
#   bool=transcript.areExonTypesSet()
#   transcript.setExonTypes() # initial-exon, internal-exon, etc...
#   transcript.setUTRtypes() # this is called by setExonTypes()
#   transcript.setExonTypes("exon")
#   success=transcript.loadExonSequences(axisSequence)
#   seq=transcript.loadTranscriptSeq(axisSequence)
#   bool=transcript.equals(other)
#   bool=transcript.overlaps(otherTranscript)
#   bool=transcript.overlaps(begin,end)
#   bool=transcript.isPartial()
#   bool=transcript.isContainedWithin(begin,end)
#   bool=transcript.contains(begin,end)
#   bool=transcript.exonOverlapsExon(exon)
#   len=transcript.getLength() # sum of exon sizes
#   len=transcript.getExtent() # end-begin
#   (begin,end)=transcript.getCDSbeginEnd() # call sortExons() first!
#                 ^ begin is always < end
#   n=transcript.numExons()
#   exon=transcript.getIthExon(i)
#   n=transcript.numUTR()
#   utr=transcript.getIthUTR(i)
#   len=transcript.totalUTRlen()
#   transcript.deleteExon(index)
#   transcript.deleteExonRef(exon)
#   transcript.recomputeBoundaries() # for after trimming 1st & last exons
#   transcript.getSubstrate()
#   transcript.getSource()
#   gff=transcript.toGff()
#   id=transcript.getID()
#   id=transcript.getTranscriptId()
#   id=transcript.getGeneId()
#   transcript.setGeneId(id)
#   transcript.setTranscriptId(id)
#   transcript.setSubstrate(substrate)
#   transcript.setSource(source)
#   begin=transcript.getBegin()
#   end=transcript.getEnd()
#   transcript.setBegin(x)
#   transcript.setEnd(x)
#   strand=transcript.getStrand()
#   transcript.setStrand(strand)
#   if(transcript.isWellFormed(sequence)): ...   # See notes in the sub
#   transcript.trimUTR()
#   transcript.getScore()
#   introns=transcript.getIntrons()
#   nextExon=transcript.getSuccessor(thisExon)
#   transcript.shiftCoords(delta)
#   transcript.reverseComplement(seqLen)
#   transcript.setStopCodons({"TGA":1,"TAA":1,"TAG":1})
#   g=transcript.getGene()
#   transcript.setGene(g)
#   genomicCoord=transcript.mapToGenome(transcriptCoord)
#   transcriptCoord=transcript.mapToTranscript(genomicCoord)
#   exon=transcript.getExonContaining(genomicCoord)
#   array=transcript.getSpliceSites()
#   array=transcript.parseExtraFields() # array of [key,value] pairs
#   hash=transcript.hashExtraFields(keyValuePairs)
#   transcript.setExtraFieldsFromKeyValuePairs(array); # [key,value]
#   transcript.setExtraFields(string)
#   transcript.parseRawExons() # infers UTR elements from exons (CDS) and
#                                rawExons
#   transcript.becomeNoncoding() # enforces all exons to be UTR
# Private methods:
#   transcript.adjustOrders()
#   transcript.sortExons()
######################################################################

class Transcript:

    validExonTypes={"single-exon":1, "initial-exon":1, "internal-exon":1,
                    "final-exon":1}

    def __init__(self,id,strand=None):
        if(type(id)!="EssexNode"): # not an EssexNode
            self.transcriptId=id
            self.strand=strand
            self.exons=[]
            self.UTR=[]
            self.stopCodons={"TAG":1,"TGA":1,"TAA":1}
        else: # EssexNode
            essex=id
            self.transcriptId=essex.getAttribute("ID")
            self.strand=essex.getAttribute("strand")
            self.source=essex.getAttribute("source")
            self.begin=essex.getAttribute("begin")
            self.end=essex.getAttribute("end")
            self.geneId=essex.getAttribute("gene")
            self.substrate=essex.getAttribute("substrate")
            self.exons=[]
            self.UTR=[]
            self.stopCodons={"TAG":1,"TGA":1,"TAA":1}
            exons=self.exons
            UTR=self.UTR
            exonsElem=essex.findChild("exons")
            if(exonsElem):
                n=exonsElem.numElements()
                for i in range(0,n):
                    exon=exonsElem.getIthElem(i)
                    begin=int(exon.getIthElem(0))
                    end=int(exon.getIthElem(1))
                    exon=Exon(begin,end,self)
                    exons.append(exon)
            utrElem=essex.findChild("UTR")
            if(utrElem):
                n=utrElem.numElements()
                for i in range(0,n):
                    exon=utrElem.getIthElem(i)
                    begin=int(exon.getIthElem(0))
                    end=int(exon.getIthElem(1))
                    exon=Exon(begin,end,self)
                    UTR.append(exon)
        
    def equals(self,other):
        if(self.getSource()!=other.getSource()): return False
        if(self.getStrand()!=other.getStrand()): return False
        if(self.getBegin()!=other.getBegin()): return False
        if(self.getEnd()!=other.getEnd()): return False
        n=self.numExons()
        m=other.numExons()
        if(n!=m): return 0
        for i in range(0,m):
            thisExon=self.getIthExon(i)
            thatExon=other.getIthExon(i)
            if(thisExon.getBegin()!=thatExon.getBegin()): return False
            if(thisExon.getEnd()!=thatExon.getEnd()): return False
        return True

    def compStrand(self,strand):
        if(strand=="+"): return "-"
        if(strand=="-"): return "+"
        if(strand=="."): return "."
        raise Exception("Unknown strand \""+strand)

    def setTranscriptId(self,newId):
        self.transcriptId=newId

    def reverseComplement(self,seqLen):
        begin=self.getBegin()
        end=self.getEnd()
        self.begin=seqLen-end
        self.end=seqLen-begin
        self.strand=self.compStrand(self.strand)
        exons=self.exons
        for exon in exons: exon.reverseComplement(seqLen)
        exons=self.UTR
        for exon in exons: exon.reverseComplement(seqLen)

    def exonOverlapsExon(self,exon):
        exons=self.exons
        n=len(exons)
        for i in range(n):
            myExon=exons[i]
            if(exon.overlaps(myExon)): return True
        return False

    def shiftCoords(self,delta):
        exons=self.exons
        for exon in exons: exon.shiftCoords(delta)
        UTR=self.UTR
        for utr in UTR: utr.shiftCoords(delta)
        self.begin+=delta
        self.end+=delta

    def loadExonSequences(self,axisSequenceRef):
        exons=self.exons
        numExons=len(exons)
        strand=self.strand
        for i in range(numExons):
            exon=exons[i]
            start=exon.begin
            length=exon.end-start
            exonSeq=axisSequenceRef[start:start+length]
            if(len(exonSeq)!=length):
                raise Exception("start="+str(start)+", length="+str(length)
                                +", but substrate "+self.substrate+
                                " ends at "+len(axisSequenceRef))
            if(strand=="-"):
                exonSeq=Translation.reverseComplement(exonSeq)
            exon.sequence=exonSeq
        return True

    def loadTranscriptSeq(self,exisSequenceRef):
        exons=self.exons
        numExons=len(exons)
        firstExon=exons[0]
        self.loadExonSequences(axisSequenceRef)
        sequence=""
        for exon in exons: sequence+=exon.sequence
        self.sequence=sequence
        return sequence

    def contains(self,begin,end):
        return self.begin<=begin and self.end>=end

    def isContainedWithin(self,begin,end):
        return self.begin>=begin and self.end<=end

    def overlaps(self,*parms):
        numParms=len(parms)
        if(numParms<1 or numParms>2): raise Exception("1 or 2 parms expected")
        if(numParms==2):
            [begin,end]=parms
            return self.begin<end and begin<self.end
        otherTranscript=parms[0]
        return self.begin<otherTranscript.end and \
            otherTranscript.begin<self.end

    def getLength(self):
        exons=self.exons
        length=0
        for exon in exons: length+=exon.getLength()
        return length

    def getExtent(self):
        return self.end-self.begin

    def numExons(self):
        return len(self.exons)

    def getIthExon(self,i):
        return self.exons[i]

    def getIthUTR(self,i):
        return self.UTR[i]

    def totalUTRlen(self):
        UTR=self.UTR
        len=0
        for utr in UTR: len+=utr.getLength()
        return len

    def deleteExon(self,index):
        exons=self.exons
        exons.pop(index)
        self.adjustOrders()

    def sortExons(self):
        rev=self.strand=="+"
        self.exons.sort(key=lambda exon: exon.begin,reverse=rev)
        self.UTR.sort(key=lambda exon: exon.begin,reverse=rev)
        self.rawExons=sort(key=lambda exon:exon.begin,reverse=rev)

    def adjustOrders(self):
        exons=self.exons
        numExons=len(exons)
        if(numExons==0): return
        for i in range(numExons):
            exons[i].order=i

    def areExonTypesSet(self):
        exons=self.exons
        for exon in exons:
            if(not Transcript.validExonTypes.get(exon.getType(),None)):
                return False
        return True

    def setExonTypes(self,defaultType=None):
        self.setUTRtypes()
        exons=self.exons
        numExons=len(exons)
        if(defaultType):
            for exon in exons: exon.setType(defaultType)
            return
        if(numExons==1):
            exon=exons[0]
            if(not Transcript.validExonTypes.get(exon.getType(),None)):
                exon.setType("single-exon")
        else:
            for exon in exons:
                if(not Transcript.validExonTypes.get(exon.getType(),None)):
                    exon.setType("interal-exon")
            exons[0].setType("initial-exon")
            exons[numExons-1].setType("final-exon")

    def setUTRtypes(self):
        if(self.numExons()==0):
            UTR=self.UTR
            for utr in UTR: utr.setType("UTR")
            return
        self.sortExons()
        (CDSbegin,CDSend)=self.getCDSbeginEnd()
        if(self.utr is None): self.utr=[]
        UTR=self.utr
        strand=self.getStrand()
        if(strand=="+"):
            for utr in UTR:
                begin=utr.getBegin()
                if(begin<CDSbegin): utr.setType("five_prime_UTR")
                else: utr.setType("three_prime_UTR")
        else:
            for utr in UTR:
                begin=utr.getBegin()
                if(begin>CDSbegin): utr.setType("five_prime_UTR")
                else: utr.setType("three_prime_UTR")

    def deleteExonRef(self,victim):
        exons=self.exons
        numExons=len(exons)
        i=0
        while(i<numExons):
            thisExon=exons[i]
            if(thisExon==victim): break
            i+=1
        if(i>=numExons):
            raise Exception("Can't find exon "+victim+
                            " in Transcript::deleteExon()")
        self.deleteExon(i)

    def recomputeBoundaries(self):
        exons=self.exons
        numExons=len(exons)
        firstExon=exons[0]
        lastExon=exons[numExons-1]
        strand=self.strand
        if(strand=="+"):
            self.begin=firstExon.begin
            self.end=lastExon.end
        else:
            self.begin=lastExon.begin
            self.end=firstExon.end
        for utr in self.UTR:
            if(utr.getBegin()<self.begin):
                self.begin=utr.getBegin()
            if(utr.getEnd()>self.end):
                self.end=utr.getEnd()

    def addExon(self,exon):
        strand=exon.getStrand()
        exons=self.exons
        exons.append(exon)
        rev=strand=="-"
        exons.sort(key=lambda exon: exon.begin,reverse=strand=="-")
        self.adjustOrders()

    def getSubstrate(self):
        return self.substrate

    def getSource(self):
        return self.source

    def toGff(self):
        transID=self.transcriptId
        geneID=self.geneId
        keyValuePairs=self.parseExtraFields()
        extraFields=""
        for pair in keyValuePairs:
            (key,value)=pair
            if(key=="gene_id" or key=="transcript_id"): continue
            extraFields+=key+"="+value+";"
        exons=self.exons
        numExons=len(exons) if exons else 0
        gff=""
        begin=self.begin
        end=self.end
        if(begin is not None):
            begin+=1 # convert to 1-based coordinates
            substrate=self.substrate
            source=self.source
            strand=self.strand
            extra=""
            if(re.search("\S",extraFields)): extra="; "+extraFields
            gff+=substrate+"\t"+source+"\ttranscript\t"+begin+"\t"+end+ \
               "\t.\t"+strand+"\t.\ttranscript_id \""+transID+ \
               "\"; gene_id \""+geneID+"\""+extra+"\n"
        for exon in exons: gff+=exon.toGff()
        UTR=self.UTR
        for exon in UTR:
            exon.type="UTR" ### ?
            gff+=exon.toGff()
        return gff

    def getTranscriptId(self):
        return self.transcriptId

    def getGeneId(self):
        return self.geneId

    def setGeneId(self,id):
        self.geneId=id

    def getID(self):
        return self.transcriptId

    def setSubstrate(self,substrate):
        self.substrate=substrate

    def setSource(self,source):
        self.source=source

    def getBegin(self):
        return self.begin

    def getEnd(self):
        return self.end

    def getStrand(self):
        return self.strand

    def isWellFormed(self,seq):
        """if(transcript.isWellFormed(sequence)) ...
        This procedure iterates through the codons of this transcript,
        starting at the start codon (attribute startCodon specifies this
        offset within the transcript, not counting intron bases), and
        continuing until either an in-frame stop codon is encountered,
        or the end of the transcript is reached.  The transcript is
        considered well-formed only if a stop-codon is encountered.
        """
        stopCodons=self.stopCodons

        # 1. Check whether any exons overlap each other
        exons=self.exons
        numExons=len(exons)
        for i in range(1,numExons):
            exon=exons[i]
            prevExon=exons[i-1]
            if(exon.overlaps(prevExon)): return 0

        # 2. Check that there is an in-frame stop-codon
        iterator=CodonIterator(self,seq,stopCodons)
        codons=iterator.getAllCodons()
        n=len(codons)
        if(n==0): return False
        lastCodon=codons[n-1]
        isStop=stopCodons.get(lastCodon.triplet,None)
        return True if isStop else False

    def trimUTR(self,axisSequenceRef):
        self.adjustOrders()
        stopCodons=self.stopCodons
        sequence=self.sequence
        strand=self.strand
        numExons=self.numExons()
        startCodon=self.startCodon
        if(not startCodon):
            raise Exception("can't trim UTR, because startCodon is not set")
        for j in(numExons):
            exon=self.getIthExon(j)
            length=exon.getLength()
            if(length<=startCodon):
                self.deleteExon(j)
                numExons-=1
                j-=1
                startCodon-=length
                self.adjustOrders() ### 4/1/03
            else:
                if(strand=="+"):
                    exon.trimInitialPortion(startCodon)
                    self.begin=exon.begin
                else:
                    exon.trimInitialPortion(startCodon)### ???
                    self.end=exon.end
                exon.type="initial-exon" if numExons>1 else "single-exon"
                self.startCodon=0
                break
        
        # Find in-frame stop codon
        codonIterator=CodonIterator(self,axisSequenceRef,stopCodons)
        stopCodonFound=False
        while(True):
            codon=codonIterator.nextCodon()
            if(not codon): break
            if(stopCodons.get(codon.triplet,None)):
                exon=codon.exon
                coord=codon.absoluteCoord
                trimBases=0
                if(strand=="+"): trimBases=exon.end-coord-3
                else: trimBases=coord-exon.begin-3
                if(trimBases>=0):
                    exon.trimFinalPortion(trimBases)
                    exon.type="single-exon" if exon.order==0 else "final-exon"
                    j=numExons-1
                    while(j>exon.order):
                        self.deleteExon(j)
                        j-=1
                    stopCodonFound=True
                    break
                else: # codon is interrupted; trim the next exon
                    nextExon=self.getSuccessor(exon)
                    if(not nextExon):
                        raise Exception("exon successor not found")
                    nextExon.trimFinalPortion(nextExon.getLength()+trimBases)
                    nextExon.type="final-exon"
                    j=numExons-1
                    while(j>nextExon.order):
                        self.deleteExon(j)
                        j-=1
                    stopCodonFound=True
                    break	
        if(not stopCodonFound):
            ### sometimes the GFF coords don't include the stop codon...
            numExons=self.numExons()
            lastExon=self.getIthExon(numExons-1)
            lastExonEnd=lastExon.getEnd()
            seq=axisSequenceRef
            if(strand=="+"):
                stopCodonBegin=lastExonEnd
                stopCodon=seq[stopCodonBegin:stopCodonBegin+3]
                if(stopCodon!="TAG" and stopCodon!="TAA" and stopCodon!="TGA"):
                    print("Warning!  No stop codon found for",
                          self.transcriptId,self.strand,
                          "strand , unable to trim UTR")
            else: # strand="-"
                stopCodonBegin=lastExon.getBegin()-3
                stopCodon=seq[stopCodonBegin,stopCodonBegin+3]
                stopCodon=Translation.reverseComplement(stopCodon)
                if(stopCodon!="TAG" and stopCodon!= "TAA" and stopCodon!="TGA"):
                    print("Warning!  No stop codon found for",
                          self.transcriptId,self.strand,
                          "strand , unable to trim UTR")
        self.recomputeBoundaries()
        
    def getScore(self):
        exons=self.exons
        score=0;
        for exon in exons:
            exonScore=exon.getScore()
            if(exonScore!="."): score+=exonScore
        return score

    def getIntrons(self):
        numExons=self.numExons()
        strand=self.strand
        introns=[]
        lastExonEnd=None
        for i in range(numExons):
            exon=self.getIthExon(i)
            if(lastExonEnd):
                if(strand=="+"):
                    introns.append([lastExonEnd,exon.getBegin()])
                else:
                    introns.append([exon.getEnd(),lastExonEnd])
            lastExonEnd=exon.getEnd() if strand=="+" else exon.getBegin()
        return introns

    def getSuccessor(self,targetExon):
        exons=self.exons
        numExons=len(exons)
        for i in range(numExons-1):
            exon=exons[i]
            if(exon is targetExon): return exons[i+1]
        return None

    def setStopCodons(self,stopCodons):
        self.stopCodons=stopCodons

    def isPartial(self):
        exons=self.exons
        numExons=len(exons)
        if(numExons==1): return exons[0].getType()!="single-exon"
        return exons[0].getType()!="initial-exon" or \
               exons[numExons-1].getType()!="final-exon"

    def getGene(self):
        return self.gene

    def setGene(self,g):
        self.gene=g

    def setBegin(self,x):
        self.begin=x

    def setEnd(self,x):
        self.end=x

    def mapToGenome(self,transcriptCoord):
        original=transcriptCoord
        numExons=self.numExons()
        for i in range(numExons):
            exon=self.getIthExon(i)
            exonLen=exon.getLength()
            if(transcriptCoord<exonLen):
                if(self.getStrand()=="+"):
                    return exon.getBegin()+transcriptCoord
                else: return exon.getEnd()-transcriptCoord-1
            transcriptCoord-=exonLen
        id=self.getID()
        raise Exception("coordinate is beyond transcript end: "+original+
                        " ("+id+")")

    def mapToTranscript(self,genomicCoord):
        exons=self.getRawExons()
        numExons=len(exons)
        transcriptCoord=0
        for i in range(numExons):
            exon=exons[i]
            if(exon.containsCoordinate(genomicCoord)):
                if(self.getStrand()=="+"):
                    return transcriptCoord+genomicCoord-exon.getBegin()
                else: return transcriptCoord+exon.getEnd()-genomicCoord-1
            exonLen=exon.getLength()
            transcriptCoord+=exonLen
        return -1

    def  getExonContaining(self,genomicCoord):
        numExons=self.numExons()
        for i in range(numExons):
            exon=self.getIthExon(i)
            if(exon.containsCoordinate(genomicCoord)): return exon

    def copy(self):
        return copy.deepcopy(self)

    def setStrand(self,strand):
        self.strand=strand
        exons=self.exons
        for exon in exons: exon.setStrand(strand)

    def getRawExons(self):
        exons=self.exons
        UTR=self.UTR
        rawExons=[]
        for exon in exons: rawExons.append(exon.copy())
        for utr in UTR: rawExons.append(utr.copy())
        # Sort into chromosome order (temporarily):
        rawExons.sort(key=lambda exon: exon.begin)
        # Now coalesce any UTR-exon pairs that are adjacent:
        n=len(rawExons)
        i=0
        while(i<n):
            exon=rawExons[i]
            exon.setType("exon")
            if(i+1<n):
                nextExon=rawExons[i+1]
                if(exon.getEnd()==nextExon.getBegin()):
                    exon.setEnd(nextExon.getEnd())
                    nextExon=None
                    rawExons.pop(i+1)
                    n-=1
                    i-=1
            i+=1

        # Sort into transcription order
        strand=self.getStrand()
        rawExons.sort(key=lambda exon: exon.begin,reverse=strand=="-")
        return rawExons

    def numUTR(self):
        return len(self.UTR)

    def parseExtraFields(self):
        pairs=[]
        string=self.extraFields
        fields=string.split(";")
        for field in fields:
            match=re.search("(\S+)[\s=]+(\S+)",field)
            if(not match): continue
            (key,value)=(match.group(1),match.group(2))
            match=re.search("\"(\S+)\"",value)
            if(match): value=match.group(1)
            pairs.append([key,value])
        return pairs

    def setExtraFieldsFromKeyValuePairs(self,array):
        string=""
        for pair in array:
            (key,value)=pair
            string+=key+"="+value+";"
        self.setExtraFields(string)

    def setExtraFields(self,string):
        self.extraFields=string

    def hashExtraFields(self,pairs):
        hash={}
        for pair in pairs:
            (key,value)=pair
            hash[key]=value
        return hash

    def parseRawExons(self):
        rawExons=self.rawExons
        numRaw=len(rawExons) if rawExons else 0
        if(numRaw==0): return
        CDS=self.exons
        strand=self.strand
        self.sortExons() # also sorts rawExons
        (cdsBegin,cdsEnd)=self.getCDSbeginEnd()
        if(cdsBegin<0): # noncoding gene
            if(CDS is None or len(CDS)==0): self.exons=rawExons
            return
        UTR=[]
        if(strand=="+"):
            for exon in rawExons:
                begin=exon.getBegin()
                end=exon.getEnd()
                if(begin<cdsBegin):
                    if(end<=cdsBegin):
                        newExon=exon.copy()
                        newExon.setType("five_prime_UTR")
                        UTR.append(newExon)
                    else:
                        newExon=exon.copy()
                        newExon.setEnd(cdsBegin)
                        newExon.setType("five_prime_UTR")
                        UTR.append(newExon)
                if(end>cdsEnd):
                    if(begin>=cdsEnd):
                        newExon=exon.copy()
                        newExon.setType("three_prime_UTR")
                        UTR.append(newExon)
                    else:
                        newExon=exon.copy()
                        newExon.setBegin(cdsEnd)
                        newExon.setType("three_prime_UTR")
                        UTR.append(newExon)
        else: # strand=="-"
            for exon in rawExons:
                begin=exon.getBegin()
                end=exon.getEnd()
                if(begin<cdsBegin):
                    if(end<=cdsBegin):
                        newExon=exon.copy()
                        newExon.setType("three_prime_UTR")
                        UTR.append(newExon)
                    else:
                        newExon=exon.copy()
                        newExon.setEnd(cdsBegin)
                        newExon.setType("three_prime_UTR")
                        UTR.append(newExon)
                if(end>cdsEnd):
                    if(begin>=cdsEnd):
                        newExon=exon.copy()
                        newExon.setType("five_prime_UTR")
                        UTR.append(newExon)
                    else:
                        newExon=exon.copy()
                        newExon.setBegin(cdsEnd)
                        newExon.setType("five_prime_UTR")
                        UTR.append(newExon)
        self.UTR=UTR

    def getCDSbeginEnd(self):
        CDS=self.exons
        numCDS=len(CDS)
        if(numCDS==0): return (-1,-1)
        strand=self.strand
        if(strand=="+"):
            begin=CDS[0].getBegin()
            end=CDS[numCDS-1].getEnd()
            return (begin,end)
        else: # strand=="-"
            begin=CDS[numCDS-1].getBegin()
            end=CDS[0].getEnd()
            return (begin,end)

    def becomeNoncoding(self):
        exons=self.exons
        UTR=self.UTR
        raw=self.rawExons
        combined=[]
        if(exons):
            for exon in exons: combined.append(exon)
        if(UTR):
            for exon in UTR: combined.append(exon)
        if(raw):
            for exon in raw: combined.append(exon)
        combined.sort(key=lambda exon: exon.begin)
        n=len(combined)
        i=0
        while(i<n-1):
            this=combined[i]
            next=combined[i+1]
            if(this.getEnd()>=next.getBegin()):
                if(this.getEnd()<next.getEnd()):
                    this.setEnd(next.getEnd())
                    combined.pop(i+1)
                    n-=1
                    i-=1
            i+=1
        for exon in combined: exon.setType("UTR")
        self.exons=None
        self.rawExons=None
        self.UTR=combined
