# -*- coding: utf-8 -*-


from anytree import PostOrderIter


class RelElement():
    """ Describes one of the two (or more) elements belonging to a relation """
    minID: int
    maxID: int
    isNuclear: bool
    isLeaf: bool


class Relation():
    nr: int
    name: str
    isMultiNuclear: bool
    constituent: RelElement
    attachmentPoint: RelElement
    centralSubconstituent: list


class RelTable():
    __relations: list

    def __init__(self):
        self.__relations = []

    def get(self, index: int):
        return self.__relations[index]

    def append(self, e: Relation):
        self.__relations.append(e)

    def sort(self, key):
        self.__relations.sort(key=key)

    def length(self):
        return len(self.__relations)

    def __iter__(self):
        return iter(self.__relations)

# External function definitions


def generateTableFromTree(rstTree, relationTypes) -> RelTable:
    relationsTable = RelTable()
    multinuclearRelationsToProcess: dict = {}
    for node in PostOrderIter(rstTree):
        if node.entry.relname in relationTypes:
            if relationTypes[node.entry.relname] == 'rst':
                processMonoNuclearRelation(node, relationsTable)
            elif relationTypes[node.entry.relname] == 'multinuc':
                enlistMultiNuclearRelation(node, multinuclearRelationsToProcess)
    processMultiNuclearRelations(multinuclearRelationsToProcess, relationsTable)
    relationsTable.sort(key=takeNr)
    return relationsTable


def processMonoNuclearRelation(node, relationsTable):
    newEntry = Relation()
    newEntry.isMultiNuclear = False
    newEntry.nr = node.entry.subIdRange[0]
    newEntry.name = node.entry.relname
    newEntry.constituent = extractRelElement(node, False)
    newEntry.attachmentPoint = extractRelElement(node.parent, True)
    newEntry.centralSubconstituent = []
    newEntry.centralSubconstituent.append(extractCentralSubconstituent(node))
    relationsTable.append(newEntry)


def enlistMultiNuclearRelation(node, multinuclearRelationsToProcess):
    key = node.parent
    if key not in multinuclearRelationsToProcess:
        multinuclearRelationsToProcess[key] = [node.entry.relname]
    else:
        if node.entry.relname not in multinuclearRelationsToProcess[key]:
            multinuclearRelationsToProcess[key].append(node.entry.relname)


def processMultiNuclearRelations(multinuclearRelationsToProcess, relationsTable):
    for multiNucParent in multinuclearRelationsToProcess:
        parent = multiNucParent.entry
        children = multiNucParent.children
        for relation in multinuclearRelationsToProcess[multiNucParent]:        
            processRelationForParent(parent, children, relation, relationsTable)


def processRelationForParent(parent, children, relation, relationsTable):
    childrenIdRanges = extractChildrenIdRangesForRelation(parent, children, relation)
    numRanges = len(childrenIdRanges)
    if numRanges > 1:
        for i in range(0, numRanges-1):
            C_range = childrenIdRanges[i]
            A_range = [min(childrenIdRanges[i+1]), max(childrenIdRanges[numRanges-1])]

            newEntry = Relation()
            newEntry.isMultiNuclear = True
            newEntry.nr = C_range[0]
            newEntry.name = relation

            newEntry.constituent = RelElement()
            newEntry.constituent.minID = min(C_range)
            newEntry.constituent.maxID = max(C_range)
            newEntry.constituent.isNuclear = True
            newEntry.constituent.isLeaf = (min(C_range) == max(C_range))

            newEntry.attachmentPoint = RelElement()
            newEntry.attachmentPoint.minID = min(A_range)
            newEntry.attachmentPoint.maxID = max(A_range)
            newEntry.attachmentPoint.isNuclear = True
            newEntry.attachmentPoint.isLeaf = (min(A_range) == max(A_range))

            newEntry.centralSubconstituent = []
            for child in children:
                if child.entry.relname == relation:
                    newCS = extractCentralSubconstituent(child)
                    if newCS.minID >= min(C_range):
                        newEntry.centralSubconstituent.append(newCS)
            newEntry.centralSubconstituent.sort(key=takeMinID)

            relationsTable.append(newEntry)


def extractChildrenIdRangesForRelation(parent, children, relation):
    childrenIdRanges = []
    for child in children:
        if child.entry.relname == relation:
            childrenIdRanges.append(child.entry.subIdRange)
    childrenIdRanges.sort(key=takeFirst)
    return childrenIdRanges


def extractRelElement(node, isNuclear: bool) -> RelElement:
    relElement = RelElement()
    relElement.isNuclear = isNuclear
    if hasattr(node.entry, 'leafID'):
        relElement.isLeaf = True
        relElement.minID = node.entry.leafID
        relElement.maxID = node.entry.leafID
    else:
        relElement.isLeaf = False
        relElement.minID = node.entry.subIdRange[0]
        relElement.maxID = node.entry.subIdRange[1]
    return relElement


def extractCentralSubconstituent(node):
    if(len(node.children) != 1):
        return extractRelElement(node, False)
    else:
        return extractRelElement(node.children[0], True)


def takeFirst(elem):
    return elem[0]


def takeNr(elem: Relation):
    return elem.nr


def takeMinID(elem: RelElement):
    return elem.minID
