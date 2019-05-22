from rsttace.controller import IRstInput
from rsttace.core import RstTree, RstType, RstNode
from rsttace.core.rsttree import MonoNucRelation, MultiNucRelation, Span

from errno import ENOENT
from os import strerror
from os.path import isfile
import xml.etree.ElementTree as et
from collections import defaultdict


class InvalidRstFile(Exception):
    pass


class RstTreeParser(IRstInput):
    """ Parser that reads a rs3-file and generates a RST-tree.
        File content is read into internal buffer during initialization.
        'FileNotFoundError' is raised if file does not exist."""

    def __init__(self, filePath: str):
        """ File content is read into internal buffer
            during initialization. """
        if fileExists(filePath):
            self.fileContent = readFile(filePath)
        else:
            raise FileNotFoundError(ENOENT, strerror(ENOENT), filePath)

    def read(self) -> RstTree:
        """ Reads and parses the contents of the internal buffer.
            'InvalidRstFile' is raised for wrong file format. """
        xmlData = self.fileContent.getroot()
        if 'rst' == xmlData.tag:
            relations = parseHeader(xmlData)
            segmentList = parseBody(xmlData)
            treeGenerator = TreeGenerator(relations)
            return treeGenerator.run(segmentList)
        else:
            raise InvalidRstFile("Unexpected XML root, \
                                  expected the following tag: <rst>")


class BodyEntry():
    def __init__(self, xmlEntry):
        if self.__validBodyEntry(xmlEntry):
            self.entryID = xmlEntry.get('id')
            self.parent = xmlEntry.get('parent')
            xmlRelname = xmlEntry.get('relname')
            if isinstance(xmlRelname, str):
                self.relname = xmlRelname.lower()
        else:
            raise InvalidRstFile("Invalid segment or group:\
                                  ID is missing")

    def __validBodyEntry(self, xmlEntry) -> bool:
        if xmlEntry.get('id') is not None:
            return True
        else:
            return False


class Segment(BodyEntry):
    def __init__(self, xmlEntry, segmentID: int):
        BodyEntry.__init__(self, xmlEntry)
        if self.__validSegment(xmlEntry):
            self.text = xmlEntry.text.strip('\n')
            self.segmentID = segmentID
        else:
            raise InvalidRstFile("Invalid segment or group:\
                                  Text is missing")

    def __validSegment(self, xmlEntry) -> bool:
        if xmlEntry.text is not None:
            return True
        else:
            return False


class Group(BodyEntry):
    def __init__(self, xmlEntry):
        BodyEntry.__init__(self, xmlEntry)
        if self.__validGroup(xmlEntry):
            self.type = xmlEntry.get('type')
        else:
            raise InvalidRstFile("Invalid segment or group:\
                                  Type is missing")

    def __validGroup(self, xmlEntry) -> bool:
        if xmlEntry.get('type') is not None:
            return True
        else:
            return False


rstTypeLUT = dict({'rst': RstType.MONO_NUCLEAR,
                   'multinuc': RstType.MULTI_NUCLEAR,
                   'span': RstType.SPAN})


def fileExists(filePath: str) -> bool:
    """ Checks whether the desired file exists """
    return isfile(filePath)


def readFile(filePath: str):
    """ Function reading a desired XML-file """
    try:
        return et.parse(filePath)
    except et.ParseError:
        raise InvalidRstFile("Parsing of XML file failed")


def parseHeader(xmlData) -> dict:
    for xmlBlock in xmlData:
        if 'header' == xmlBlock.tag:
            return parseRelations(xmlBlock)

    raise InvalidRstFile("XML file contains no header section")


def parseRelations(xmlBlock):
    relations = dict({'span': RstType.SPAN})
    for xmlMeta in xmlBlock:
        if 'relations' == xmlMeta.tag:
            for xmlEntry in xmlMeta:
                if 'rel' == xmlEntry.tag:
                    try:
                        rel_name = xmlEntry.get('name').lower()
                        rel_type = xmlEntry.get('type')
                        relations[rel_name] = rstTypeLUT[rel_type]
                    except KeyError:
                        raise InvalidRstFile("Invalid relation encoding")
                else:
                    raise InvalidRstFile("Invalid tag in header")

    return relations


def parseBody(xmlData) -> list:
    for xmlBlock in xmlData:
        if 'body' == xmlBlock.tag:
            entryList = []
            currentSegmentID = 0

            for entry in xmlBlock:
                if 'segment' == entry.tag:
                    currentSegmentID += 1
                    entryList.append(Segment(entry, currentSegmentID))
                elif 'group' == entry.tag:
                    entryList.append(Group(entry))
                else:
                    raise InvalidRstFile("Invalid tag in body")

            return entryList

    raise InvalidRstFile("XML file contains no body section")


class TreeGenerator():
    def __init__(self, relations: dict):
        self.relations = relations
        self.monoNucs = []
        self.multiNucs = []

    def run(self, segments: list) -> RstTree:
        rootID = self.__createDictionaries(segments)
        if rootID is None:
            return RstTree(self.relations, None, [], [])
        else:
            rootNode = RstNode()
            self.__appendDependencies(rootID, rootNode)
            return RstTree(self.relations,
                           rootNode,
                           self.monoNucs,
                           self.multiNucs)

    def __createDictionaries(self, segments):
        """ Dictionaries of lists, encoding children and siblings of each node:
            Key = ID of node, Value = List with children/siblings IDs """

        rootID = None
        self.segmentDict = {}
        self.siblingDict = {}
        self.childrenDict = defaultdict(list)

        for entry in segments:
            self.segmentDict[entry.entryID] = entry
            if entry.parent is not None:
                if RstType.MONO_NUCLEAR == self.relations[entry.relname]:
                    if not self.siblingDict.__contains__(entry.parent):
                        self.siblingDict[entry.parent] = entry.entryID
                    else:
                        raise InvalidRstFile("Multiple mono nuclear relations\
                                              for single element")
                else:
                    self.childrenDict[entry.parent].append(entry.entryID)
            else:
                if rootID is None:
                    rootID = entry.entryID
                else:
                    raise InvalidRstFile("Multiple root elements\
                                          have been found")

        return rootID

    def __appendDependencies(self, nodeID: int, rstNode: RstNode):
        nodeXML: BodyEntry = self.segmentDict[nodeID]
        # process siblings
        if self.siblingDict.__contains__(nodeID):
            siblingID = self.siblingDict[nodeID]
            siblingXML: BodyEntry = self.segmentDict[siblingID]
            siblingNode = createNewNode(siblingXML)
            # create mono nuclear relation between siblings
            monoNuc = MonoNucRelation(siblingXML.relname,
                                      siblingNode, rstNode)
            rstNode.toSibling = monoNuc
            siblingNode.toSibling = monoNuc
            self.monoNucs.append(monoNuc)
            # add sibling of node to parent (if existent)
            if isinstance(rstNode.toParent, Span):
                siblingNode.toParent = rstNode.toParent
                rstNode.toParent.children.append(siblingNode)
            # recursive call for lower levels
            self.__appendDependencies(siblingID, siblingNode)

        # process children
        childrenIDs = self.childrenDict[nodeID]
        if len(childrenIDs) > 0:
            childrenNodes = []
            relname = ""
            for childID in childrenIDs:
                childXML: BodyEntry = self.segmentDict[childID]
                childNode = createNewNode(childXML)
                childrenNodes.append(childNode)
                # check that all children belong to the same relation
                if "" == relname:
                    relname = childXML.relname
                elif relname != childXML.relname:
                    raise InvalidRstFile("Different relation names in\
                                          one multi nuclear relation")
            #   create new relation between node and children
            if RstType.SPAN == self.relations[relname]:
                span = Span(rstNode, childrenNodes)
                rstNode.toChildren = span
                for childNode in childrenNodes:
                    childNode.toParent = span
            elif RstType.MULTI_NUCLEAR == self.relations[relname]:
                multiNuc = MultiNucRelation(relname, rstNode, childrenNodes)
                rstNode.toChildren = multiNuc
                for childNode in childrenNodes:
                    childNode.toParent = multiNuc
                self.multiNucs.append(multiNuc)
            else:
                raise InvalidRstFile("Found relation with unspecified type")
            # recursive call for lower levels
            for childID, childNode in zip(childrenIDs, childrenNodes):
                self.__appendDependencies(childID, childNode)

        # sort children & build segment ID range (based on child segment IDs)
        if rstNode.toChildren is not None:
            children = rstNode.toChildren.children
            children.sort(key=lambda child: min(child.segmentID))
            rstNode.segmentID = [min(children[0].segmentID),
                                 max(children[-1].segmentID)]

        # check correctness of xml entry type and rst tree node type
        if isinstance(rstNode.toChildren, Span):
            correct = isinstance(nodeXML, Group) and 'span' == nodeXML.type
        elif isinstance(rstNode.toChildren, MultiNucRelation):
            correct = isinstance(nodeXML, Group) and 'multinuc' == nodeXML.type
        elif rstNode.toChildren is None:
            correct = isinstance(nodeXML, Segment)
        else:
            correct = False

        if not correct:
            raise InvalidRstFile("Entry has wrong group or segment type")
        else:
            return


def createNewNode(xmlElement: BodyEntry) -> RstNode:
    newNode = RstNode()
    if isinstance(xmlElement, Segment):
        newNode.text = xmlElement.text
        newNode.segmentID = [xmlElement.segmentID]
    return newNode
