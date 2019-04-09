from enum import IntEnum
from typing import List


class RstType(IntEnum):
    MONO_NUCLEAR = 0
    MULTI_NUCLEAR = 1
    SPAN = 2


class RstNode():
    """ Class encoding a tree node """
    toParent = None
    toSibling = None
    toChildren = None
    text = None
    segmentID = None


class MonoNucRelation():
    """ Class encoding mononuclear relations """
    def __init__(self,
                 relation: str,
                 start: RstNode,
                 end: RstNode):
        self.relation = relation
        self.start = start
        self.end = end


class MultiNucRelation():
    """ Class encoding multinuclear relations """
    def __init__(self,
                 relation: str,
                 parent: RstNode,
                 children: List[RstNode]):
        self.relation = relation
        self.parent = parent
        self.children = children


class Span():
    """ Class encoding spans """
    def __init__(self,
                 parent: RstNode,
                 children: List[RstNode]):
        self.parent = parent
        self.children = children


class RstTree():
    def __init__(self,
                 relations: dict,
                 rootNode: RstNode,
                 monoNucs: List[MonoNucRelation],
                 multiNucs: List[MultiNucRelation]):
        self.relations = relations
        self.root = rootNode
        self.monoNucs = monoNucs
        self.multiNucs = multiNucs
        return
