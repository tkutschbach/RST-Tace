# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 00:49:01 2018

@author: tinokuba
"""
from abc import ABC, abstractmethod
from rsttace.core import RstTree, RelTable, ComparisonTable, CompareSetTable
from rsttace.core import TableGenerator, TableComparer, TableSetComparer

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


class ICompareSetTableOutput(ABC):
    @abstractmethod
    def write(self, compSetTable: CompareSetTable):
        pass
