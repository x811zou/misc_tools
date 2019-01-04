#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# 2018 William H. Majoros (bmajoros@allumni.duke.edu)
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)

#=========================================================================
# Attributes:
#   ID = read identifier
#   refName = name of reference sequence the read aligns to
#   refPos = position in reference where alignment begins
#   CIGAR = CigarString
#   seq = read sequence
# Instance Methods:
#   rec=SamReader(ID,refName,refPos,cigar,seq)
# Class Methods:
#=========================================================================
class SamRecord:
    """SamRecord"""
    def __init__(self,ID,refName,refPos,CIGAR,seq,flags):
        self.ID=ID
        self.refName=refName
        self.refPos=refPos
        self.CIGAR=CIGAR
        self.seq=seq
        self.flags=flags

    def flag_hasMultipleSegments(self):
        return bool(self.flags & 0x1)

    def flag_properlyAligned(self):
        return bool(self.flags & 0x2)

    def flag_unmapped(self):
        return bool(self.flags & 0x4)

    def flag_nextSegmentUnmapped(self):
        return bool(self.flags & 0x8)

    def flag_revComp(self):
        return bool(self.flags & 0x10)

    def flag_nextSegmentRevComp(self):
        return bool(self.flags & 0x20)

    def flag_firstOfPair(self):
        return bool(self.flags & 0x40)

    def flag_secondOfPair(self):
        return bool(self.flags & 0x80)

    def flag_secondaryAlignment(self):
        return bool(self.flags & 0x100)

    def flag_failedFilters(self):
        return bool(self.flags & 0x200)

    def flag_PCRduplicate(self):
        return bool(self.flags & 0x400)

    def flag_supplAlignment(self):
        return bool(self.flags & 0x800)

# FLAGS:
#   0x1 template having multiple segments in sequencing
#   0x2 each segment properly aligned according to the aligner
# > 0x4 segment unmapped
# > 0x8 next segment in the template unmapped
# > 0x10 SEQ being reverse complemented
#   0x20 SEQ of the next segment in the template being reverse complemented
# > 0x40 the first segment in the template
# > 0x80 the last segment in the template
#   0x100 secondary alignment
#   0x200 not passing filters, such as platform/vendor quality controls
# > 0x400 PCR or optical duplicate
#   0x800 supplementary alignment

# M03884:303:000000000-C4RM6:1:1101:1776:15706    99      chrX:31786371-31797409  6687    44      150M    =       6813    271     ATACTATTGCTGCGGTAATAACTGTAACTGCAGTTACTATTTAGTGATTTGTATGTAGATGTAGATGTAGTCTATGTCAGACACTATGCTGAGCATTTTATGGTTGCTATGTACTGATACATACAGAAACAAGAGGTACGTTCTTTTACA  BBBBFFFFFFFGGGGGEFGGFGHFHFFFHHHFFHHHFHFHHHGFHEDGGHFHBGFHGBDHFHFFFHHHHFHHHHHGHGFFBGGGHFHFFHHFFFFHHHHGHGFHHGFHGHHHGFHFFHHFHHFFGFFFFGGEHFFEHHFGHHHGHHHHFB  AS:i:300        XN:i:0  

