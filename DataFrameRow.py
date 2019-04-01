#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# 2018 William H. Majoros (bmajoros@alumni.duke.edu)
#=========================================================================
from __future__ import (absolute_import, division, print_function, 
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
import sys

#=========================================================================
# Attributes:
#   label : string
#   values : array of values
# Methods:
#   row=DataFrameRow()
#   elem=row[i] # first element is at 0 (the label is not counted)
#   label=row.getLabel()
#   row.rename(label)
#   n=row.length()
#   row.toInt()
#   row.toFloat()
#   row.append(value)
#   row.print(handle)
#=========================================================================

class DataFrameRow:
   def __init__(self):
      self.label=""
      self.values=[]

   def __getitem__(self,i):
      return self.values[i]

   def __setitem__(self,i,value):
      self.values[i]=value

   def print(self,handle):
      print(self.label+"\t","\t".join([str(x) for x in self.values]),sep="")

   def append(self,value):
      self.values.append(value)

   def length(self):
      return len(self.values)

   def getLabel(self):
      return self.label

   def rename(self,x):
      self.label=x
      
   def toInt(self):
      self.values=[int(x) for x in self.values]

   def toFloat(self):
      self.values=[float(x) for x in self.values]

