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
from DataFrameRow import DataFrameRow

#=========================================================================
# Attributes:
#   header
#   matrix : array of rows, each of which is an array of data values
#   rowHash : dictionary mapping row names to row indices
#   colHash : dictionary mapping column names to column indices
# Methods:
#   df=DataFrame()
#   rowNames=df.getRowNames()
#   colNames=df.getColumnNames()
#   n=df.nrow()
#   n=df.ncol()
#   row=df[index]
#   elem=df[i][j]
#   df.toInt()
#   df.toFloat()
#   header=df.getHeader()
#   df.hashRowNames()
#   df.hashColNames()
#   row=df.getRow(rowName) # call hashRowNames() first!
#   col=df.getColumn(columnName) # call hashColNames() first!
#   bool=df.rowExists(rowName) # call hashRowNames() first!
#   bool=df.columnExists(colName) # call hashColNames() first!
# Class methods:
#   df=DataFrame.readTable(filename,hasHeader=True,hasRowNames=True)
#=========================================================================

class DataFrame:
   def __init__(self):
      self.header=[]
      self.matrix=[]
      self.rowHash=None
      self.colHash=None

   def rowExists(self,rowName):
      if(self.rowHash is None): raise Exception("call hashRowNames() first")
      return self.rowHash.get(rowName,None) is not None

   def columnExists(self,colName):
      if(self.colHash is None): raise Exception("call hashColNames() first")
      return self.colHash.get(colName,None) is not None

   def getRowNames(self):
      names=[]
      for row in self.matrix:
         names.append(row.label)
      return names

   def getColumnNames(self):
      return header

   def getRow(self,rowName):
      if(self.rowHash is None): raise Exception("call hashRowNames() first")
      rowIndex=self.rowHash.get(rowName,None)
      if(rowIndex is None): raise Exception("row not found: "+rowName)
      return self.matrix[rowIndex]

   def getColumn(self,colName):
      if(self.colHash is None): raise Exception("call hashColNames() first")
      colIndex=self.colHash.get(colName,None)
      if(colIndex is None): raise Exception("column not found: "+colName)
      column=DataFrameRow()
      column.label=colName
      for row in self.matrix:
         colum.values.append(row[colIndex])

   def hashRowNames(self):
      h=self.rowHash={}
      numRows=self.nrow()
      for i in range(numRows):
         row=self.matrix[i]
         h[row.label]=i

   def hashColNames(self):
      h=self.colHash={}
      numCols=self.ncol()
      for i in range(numCols):
         h[header[i]]=i

   def getHeader(self):
      return self.header

   def nrow(self):
      return len(self.matrix)

   def ncol(self):
      return len(self.header)

   def __getitem__(self,i):
      return self.matrix[i]

   def toInt(self):
      for row in self.matrix: row.toInt()

   def toFloat(self):
      for row in self.matrix: row.toFloat()

   @classmethod
   def readTable(cls,filename,hasHeader=True,hasRowNames=True):
      df=DataFrame()
      with open(filename,"rt") as IN:
         if(hasHeader):
            df.header=IN.readline()
            df.header=df.header.rstrip().split()
         for line in IN:
            fields=line.rstrip().split()
            if(len(fields)<1): continue
            label=""
            if(hasRowNames):
               label=fields[0]
               fields=fields[1:]
            row=DataFrameRow()
            row.label=label
            row.values=fields
            df.matrix.append(row)
      if(len(df.matrix)>0 and df.matrix[0].length()<len(df.header)):
         df.header=df.header[1:]
      return df

