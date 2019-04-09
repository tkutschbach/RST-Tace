from .rsttree import RstTree, RstNode, Span, MonoNucRelation
from .relationstable import RelTable, Relation, RelElement

from collections import deque


class TableGenerator():
    def __init__(self):
        return

    def run(self, rstTree: RstTree) -> RelTable:
        relTable = RelTable()

        # process mono-nuclear relations
        for monoNuc in rstTree.monoNucs:
            cs = extractCentralSubconstituent(nodes=[monoNuc.start],
                                              isNuclear=False)
            relation = Relation()
            relation.isMultiNuclear = False
            relation.name = monoNuc.relation
            relation.constituent = extractRelElement(node=monoNuc.start,
                                                     isNuclear=False)
            relation.attachmentPoint = extractRelElement(node=monoNuc.end,
                                                         isNuclear=True)
            relation.centralSubconstituent = cs
            relTable.append(relation)

        # process multi-nuclear relations
        for multiNuc in rstTree.multiNucs:
            remainingNodes = deque(multiNuc.children)
            while len(remainingNodes) > 1:
                cs = extractCentralSubconstituent(nodes=remainingNodes,
                                                  isNuclear=True)
                currentNode = remainingNodes.popleft()
                pseudoNode = createPseudoNode(remainingNodes)

                relation = Relation()
                relation.name = multiNuc.relation
                relation.isMultiNuclear = True
                relation.centralSubconstituent = cs
                relation.constituent = extractRelElement(node=currentNode,
                                                         isNuclear=True)
                relation.attachmentPoint = extractRelElement(node=pseudoNode,
                                                             isNuclear=True)
                relTable.append(relation)

        return relTable


def extractRelElement(node: RstNode, isNuclear: bool) -> RelElement:
    relElement = RelElement()
    relElement.minID = min(node.segmentID)
    relElement.maxID = max(node.segmentID)
    relElement.isLeaf = (node.text is not None)
    relElement.isNuclear = isNuclear
    return relElement


def createPseudoNode(nodes: list) -> RstNode:
    """ Creates a pseudo node as a representant of a list of nodes
        for generation of attachment point in multi-nuclear relations """
    if len(nodes) > 1:
        ids = []
        for node in nodes:
            for id in node.segmentID:
                ids.append(id)

        pseudoNode = RstNode()
        pseudoNode.segmentID = [min(ids), max(ids)]
        return pseudoNode
    else:
        return nodes[0]


def extractCentralSubconstituent(nodes: list, isNuclear: bool):
    cs = []
    for node in nodes:
        monoNucRel = extractMonoNuclearRelation(node)
        if monoNucRel is not None:
            relElem = extractRelElement(node=monoNucRel.end,
                                        isNuclear=True)
        else:
            relElem = extractRelElement(node, isNuclear)
        cs.append(relElem)
    return cs


def extractMonoNuclearRelation(node: RstNode) -> MonoNucRelation:
    hasSpanBelow = isinstance(node.toChildren, Span)
    if hasSpanBelow:
        return node.toChildren.children[0].toSibling
    else:
        return None
