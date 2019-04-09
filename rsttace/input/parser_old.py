# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 16:34:33 2018

@author: tinokuba
"""

from rstTace.core import RstTree
from rstTace.controller import IRstInput
from errno import ENOENT
from os import strerror
from os.path import isfile

import xml.etree.ElementTree as ET
from anytree import AnyNode, RenderTree


class RstTreeParser(IRstInput):
    def __init__(self, filePath: str):
        if isfile(filePath):
            self.filePath = filePath
        else:
            raise FileNotFoundError(ENOENT, strerror(ENOENT), filePath)

    def read(self) -> RstTree:
        (rstTree, relationTypes) = parseInputFile(self.filePath)
        return RstTree(rstTree, relationTypes)


### External function definitions
def parseInputFile(fileString):
    xmlData         = readInputFile(fileString)
    relationTypes   = parseRelationTypes(xmlData)
    segmentList     = createSegmentList(xmlData)
    rstTree         = createTreeFromList(segmentList,relationTypes)
    #printTree(rstTree)
    return (rstTree,relationTypes)

### Type definitions
class Entry:
    def __init__(self, xmlEntry):
        self.segmentID  = xmlEntry.get('id')
        self.parent     = xmlEntry.get('parent')
        self.relname    = xmlEntry.get('relname')

class Segment(Entry):
    def __init__(self, xmlEntry, leafID):
        Entry.__init__(self, xmlEntry)
        self.leafID     = leafID
        self.text       = xmlEntry.text.strip('\n')
        self.idRange    = None
        self.subIdRange = None

class Group(Entry):
    def __init__(self, xmlEntry):
        Entry.__init__(self, xmlEntry)
        self.idRange    = None
        self.subIdRange = None

### Internal function definitions
def readInputFile(fileString):
    tree = ET.parse(fileString)
    return tree.getroot()

def parseRelationTypes(xmlData):
    relationTypes = {}
    for xmlBlock in xmlData:
        if xmlBlock.tag == 'header':
            for xmlMeta in xmlBlock:
                if xmlMeta.tag == 'relations':
                    for xmlEntry in xmlMeta:
                        if xmlEntry.tag == 'rel':
                            rel_name = xmlEntry.get('name')
                            rel_type = xmlEntry.get('type')
                            relationTypes[rel_name] = rel_type
    return relationTypes

def createSegmentList(xmlData):
    entryList = []
    currentLeafID = 0
    for xmlBlock in xmlData:
        if xmlBlock.tag == 'body':
            for entry in xmlBlock:
                if entry.tag == 'segment':
                    currentLeafID += 1
                    entryList.append(Segment(entry,currentLeafID))
                else:
                    entryList.append(Group(entry))
    return entryList

def createTreeFromList(segmentList,relationTypes):
    globalRoot = None
    treeNodeList = {}
    # TODO: potential inifinite loop
    while len(segmentList) > 0:
        for entry in segmentList:
            if (entry.parent is None) or (entry.parent in treeNodeList):
                if globalRoot is None:
                    treeNodeList[entry.segmentID] = AnyNode(entry=entry)
                    globalRoot = treeNodeList[entry.segmentID]
                else:
                    treeNodeList[entry.segmentID] = AnyNode(entry=entry, parent=treeNodeList[entry.parent])
                segmentList.remove(entry)
    labelIdRanges(globalRoot,relationTypes)
    return globalRoot

def labelIdRanges(rootNode,relationTypes):
    idList = []
    subIdList = []
    if hasattr(rootNode.entry,'leafID'):
        idList.append(rootNode.entry.leafID)
        subIdList.append(rootNode.entry.leafID)
    
    for child in rootNode.children:
        labelIdRanges(child,relationTypes)
        if child.entry.idRange is not None:
            idList = idList + child.entry.idRange
            if child.entry.relname not in relationTypes or relationTypes[child.entry.relname] != 'rst':
                subIdList = subIdList + child.entry.idRange

    if len(idList) > 0:
        while min(idList) == -1 :
            idList.remove(-1)
        rootNode.entry.idRange = [min(idList),max(idList)]
        rootNode.entry.subIdRange = [min(subIdList),max(subIdList)]
    else:
        rootNode.entry.idRange = [-1,-1]
        rootNode.entry.subIdRange = [-1,-1]        
    return

def printTree(root):
    for pre, fill, node in RenderTree(root, childiter=sortChildren):
        if hasattr(node.entry,'text'):
            print("%s%s (%d): %s" % (pre, node.entry.relname, node.entry.leafID, node.entry.text))
        else:
            print("%s%s (%s)" % (pre, node.entry.relname, node.entry.subIdRange))
            
def sortChildren(children):
    return sorted(children, key=lambda child: min(child.entry.subIdRange) )