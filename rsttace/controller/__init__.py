# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 00:49:01 2018

@author: tinokuba
"""
from abc import ABC, abstractmethod
from rsttace.core import RstTree, RelTable, ComparisonTable
from rsttace.core import TableGenerator, TableEvaluator

# Interface definitions ######################################################


class IRstInput(ABC):
    @abstractmethod
    def read(self) -> RstTree:
        pass


class IRelTableOutput(ABC):
    @abstractmethod
    def write(self, relTable: RelTable):
        pass


class IComparisonTableOutput(ABC):
    @abstractmethod
    def write(self, compTable: ComparisonTable):
        pass


# Use-Case Interactor definition #############################################


class Interactor():
    tableGenerator: TableGenerator
    tableEvaluator: TableEvaluator

    def __init__(self,
                 rstIn1: IRstInput,
                 rstIn2: IRstInput,
                 relTableOut1: IRelTableOutput,
                 relTableOut2: IRelTableOutput,
                 compTableOut: IComparisonTableOutput):

        self.tableGenerator = TableGenerator()
        self.tableEvaluator = TableEvaluator()

        self.rstReader1 = rstIn1
        self.rstReader2 = rstIn2
        self.relTableWriter1 = relTableOut1
        self.relTableWriter2 = relTableOut2
        self.compTableWriter = compTableOut

        return

    def run(self):
        relTable1 = self.tableGenerator.run(self.rstReader1.read())
        relTable2 = self.tableGenerator.run(self.rstReader2.read())
        self.relTableWriter1.write(relTable1)
        self.relTableWriter2.write(relTable2)
        compTable = self.tableEvaluator.run(relTable1, relTable2)
        self.compTableWriter.write(compTable)
        return
