# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 14:46:59 2018

@author: tinokuba
"""

from unittest import TestCase, skip
from rsttace.core import TableGenerator, TableEvaluator, ComparisonTable
from rsttace.core import RstTree, RstNode, RelTable, RstType
from rsttace.core import Relation
from rsttace.core.rsttree import MonoNucRelation, MultiNucRelation, Span


class TestTableGenerator(TestCase):
    def test_forEmptyRstTree(self):
        """ Given an empty RstTree, the TableGenerator shall return
            an empty RelationsTable """
        # Build
        emptyRstTree = RstTree({}, None, [], [])
        tableGenerator = TableGenerator()
        # Operate
        relTable = tableGenerator.run(emptyRstTree)
        # Check
        self.assertIsInstance(relTable, RelTable)
        self.assertEqual(relTable.length(), 0)

    def test_forTreeWithOneMonoNuc(self):
        # Build
        rootNode = RstNode()
        rootNode.text = "A"
        rootNode.segmentID = [1]

        siblingNode = RstNode()
        siblingNode.text = "B"
        siblingNode.segmentID = [2]

        monoNuc = MonoNucRelation("mono", siblingNode, rootNode)
        rootNode.toSibling = monoNuc
        siblingNode.toSibling = monoNuc

        tree = RstTree({"mono": RstType.MONO_NUCLEAR},
                       rootNode,
                       [monoNuc],
                       [])

        # Operate
        tableGenerator = TableGenerator()
        resultTable = tableGenerator.run(tree)

        # Check
        self.assertEqual(1, resultTable.length())

        relation: Relation = resultTable.get(0)
        self.assertEqual("mono", relation.name)
        self.assertEqual(False, relation.isMultiNuclear)

        self.assertEqual(1, relation.attachmentPoint.minID)
        self.assertEqual(1, relation.attachmentPoint.maxID)
        self.assertEqual(True, relation.attachmentPoint.isNuclear)
        self.assertEqual(True, relation.attachmentPoint.isLeaf)

        self.assertEqual(2, relation.constituent.minID)
        self.assertEqual(2, relation.constituent.maxID)
        self.assertEqual(False, relation.constituent.isNuclear)
        self.assertEqual(True, relation.constituent.isLeaf)

        self.assertEqual(1, len(relation.centralSubconstituent))
        self.assertEqual(2, relation.centralSubconstituent[0].minID)
        self.assertEqual(2, relation.centralSubconstituent[0].maxID)
        self.assertEqual(False, relation.centralSubconstituent[0].isNuclear)
        self.assertEqual(True, relation.centralSubconstituent[0].isLeaf)

    def test_forTreeWithOneMonoAndMultiNuc(self):
        # Build
        nodeA = RstNode()
        nodeA.text = "A"
        nodeA.segmentID = [1]

        nodeB = RstNode()
        nodeB.text = "B"
        nodeB.segmentID = [2]

        nodeC = RstNode()
        nodeC.text = "C"
        nodeC.segmentID = [3]

        nodeD = RstNode()
        nodeD.text = "D"
        nodeD.segmentID = [4]

        nodeBCD = RstNode()
        nodeBCD.segmentID = [2, 4]

        monoNuc = MonoNucRelation("mono", nodeBCD, nodeA)
        nodeA.toSibling = monoNuc
        nodeBCD.toSibling = monoNuc

        multiNuc = MultiNucRelation("multi", nodeBCD, [nodeB, nodeC, nodeD])
        nodeBCD.toChildren = multiNuc
        nodeB.toParent = multiNuc
        nodeC.toParent = multiNuc
        nodeD.toParent = multiNuc

        tree = RstTree({"mono": RstType.MONO_NUCLEAR,
                        "multi": RstType.MULTI_NUCLEAR},
                       nodeA,
                       [monoNuc],
                       [multiNuc])

        # Operate
        tableGenerator = TableGenerator()
        resultTable = tableGenerator.run(tree)

        # Check
        self.assertEqual(3, resultTable.length())

        monoRel: Relation = resultTable.get(0)
        self.assertEqual("mono", monoRel.name)
        self.assertEqual(False, monoRel.isMultiNuclear)
        self.assertEqual(1, monoRel.attachmentPoint.minID)
        self.assertEqual(1, monoRel.attachmentPoint.maxID)
        self.assertEqual(True, monoRel.attachmentPoint.isNuclear)
        self.assertEqual(True, monoRel.attachmentPoint.isLeaf)
        self.assertEqual(2, monoRel.constituent.minID)
        self.assertEqual(4, monoRel.constituent.maxID)
        self.assertEqual(False, monoRel.constituent.isNuclear)
        self.assertEqual(False, monoRel.constituent.isLeaf)
        self.assertEqual(1, len(monoRel.centralSubconstituent))
        self.assertEqual(2, monoRel.centralSubconstituent[0].minID)
        self.assertEqual(4, monoRel.centralSubconstituent[0].maxID)
        self.assertEqual(False, monoRel.centralSubconstituent[0].isNuclear)
        self.assertEqual(False, monoRel.centralSubconstituent[0].isLeaf)

        multiRel1: Relation = resultTable.get(1)
        self.assertEqual("multi", multiRel1.name)
        self.assertEqual(True, multiRel1.isMultiNuclear)
        self.assertEqual(3, len(multiRel1.centralSubconstituent))

        self.assertEqual(2, multiRel1.centralSubconstituent[0].minID)
        self.assertEqual(2, multiRel1.centralSubconstituent[0].maxID)
        self.assertEqual(True, multiRel1.centralSubconstituent[0].isNuclear)
        self.assertEqual(True, multiRel1.centralSubconstituent[0].isLeaf)
        self.assertEqual(3, multiRel1.centralSubconstituent[1].minID)
        self.assertEqual(3, multiRel1.centralSubconstituent[1].maxID)
        self.assertEqual(True, multiRel1.centralSubconstituent[1].isNuclear)
        self.assertEqual(True, multiRel1.centralSubconstituent[1].isLeaf)
        self.assertEqual(4, multiRel1.centralSubconstituent[2].minID)
        self.assertEqual(4, multiRel1.centralSubconstituent[2].maxID)
        self.assertEqual(True, multiRel1.centralSubconstituent[2].isNuclear)
        self.assertEqual(True, multiRel1.centralSubconstituent[2].isLeaf)

        self.assertEqual(2, multiRel1.constituent.minID)
        self.assertEqual(2, multiRel1.constituent.maxID)
        self.assertEqual(True, multiRel1.constituent.isNuclear)
        self.assertEqual(True, multiRel1.constituent.isLeaf)
        self.assertEqual(3, multiRel1.attachmentPoint.minID)
        self.assertEqual(4, multiRel1.attachmentPoint.maxID)
        self.assertEqual(True, multiRel1.attachmentPoint.isNuclear)
        self.assertEqual(False, multiRel1.attachmentPoint.isLeaf)

        multiRel2: Relation = resultTable.get(2)
        self.assertEqual("multi", multiRel2.name)
        self.assertEqual(True, multiRel2.isMultiNuclear)
        self.assertEqual(2, len(multiRel2.centralSubconstituent))

        self.assertEqual(3, multiRel2.centralSubconstituent[0].minID)
        self.assertEqual(3, multiRel2.centralSubconstituent[0].maxID)
        self.assertEqual(True, multiRel2.centralSubconstituent[0].isNuclear)
        self.assertEqual(True, multiRel2.centralSubconstituent[0].isLeaf)
        self.assertEqual(4, multiRel2.centralSubconstituent[1].minID)
        self.assertEqual(4, multiRel2.centralSubconstituent[1].maxID)
        self.assertEqual(True, multiRel2.centralSubconstituent[1].isNuclear)
        self.assertEqual(True, multiRel2.centralSubconstituent[1].isLeaf)

        self.assertEqual(3, multiRel2.constituent.minID)
        self.assertEqual(3, multiRel2.constituent.maxID)
        self.assertEqual(True, multiRel2.constituent.isNuclear)
        self.assertEqual(True, multiRel2.constituent.isLeaf)
        self.assertEqual(4, multiRel2.attachmentPoint.minID)
        self.assertEqual(4, multiRel2.attachmentPoint.maxID)
        self.assertEqual(True, multiRel2.attachmentPoint.isNuclear)
        self.assertEqual(True, multiRel2.attachmentPoint.isLeaf)

    def test_forTreeWithOneMonoSpanAndMultiNuc(self):
        # Build
        nodeA = RstNode()
        nodeA.text = "A"
        nodeA.segmentID = [1]

        nodeB = RstNode()
        nodeB.text = "B"
        nodeB.segmentID = [2]

        nodeC = RstNode()
        nodeC.text = "C"
        nodeC.segmentID = [3]

        nodeD = RstNode()
        nodeD.text = "D"
        nodeD.segmentID = [4]

        nodeAB = RstNode()
        nodeAB.segmentID = [1, 2]

        rootNode = RstNode()
        rootNode.segmentID = [1, 4]

        monoNuc = MonoNucRelation(relation="mono",
                                  start=nodeB,
                                  end=nodeA)
        nodeA.toSibling = monoNuc
        nodeB.toSibling = monoNuc

        span = Span(parent=nodeAB,
                    children=[nodeA, nodeB])
        nodeAB.toChildren = span
        nodeA.toParent = span
        nodeB.toParent = span

        multiNuc = MultiNucRelation(relation="multi",
                                    parent=rootNode,
                                    children=[nodeAB, nodeC, nodeD])
        rootNode.toChildren = multiNuc
        nodeAB.toParent = multiNuc
        nodeC.toParent = multiNuc
        nodeD.toParent = multiNuc

        tree = RstTree(relations={"mono": RstType.MONO_NUCLEAR,
                                  "multi": RstType.MULTI_NUCLEAR},
                       rootNode=rootNode,
                       monoNucs=[monoNuc],
                       multiNucs=[multiNuc])

        # Operate
        tableGenerator = TableGenerator()
        resultTable = tableGenerator.run(tree)

        # Check
        self.assertEqual(3, resultTable.length())

        monoRel: Relation = resultTable.get(0)
        self.assertEqual("mono", monoRel.name)
        self.assertEqual(False, monoRel.isMultiNuclear)
        self.assertEqual(1, monoRel.attachmentPoint.minID)
        self.assertEqual(1, monoRel.attachmentPoint.maxID)
        self.assertEqual(True, monoRel.attachmentPoint.isNuclear)
        self.assertEqual(True, monoRel.attachmentPoint.isLeaf)
        self.assertEqual(2, monoRel.constituent.minID)
        self.assertEqual(2, monoRel.constituent.maxID)
        self.assertEqual(False, monoRel.constituent.isNuclear)
        self.assertEqual(True, monoRel.constituent.isLeaf)
        self.assertEqual(1, len(monoRel.centralSubconstituent))
        self.assertEqual(2, monoRel.centralSubconstituent[0].minID)
        self.assertEqual(2, monoRel.centralSubconstituent[0].maxID)
        self.assertEqual(False, monoRel.centralSubconstituent[0].isNuclear)
        self.assertEqual(True, monoRel.centralSubconstituent[0].isLeaf)

        multiRel1: Relation = resultTable.get(1)
        self.assertEqual("multi", multiRel1.name)
        self.assertEqual(True, multiRel1.isMultiNuclear)
        self.assertEqual(3, len(multiRel1.centralSubconstituent))

        self.assertEqual(1, multiRel1.centralSubconstituent[0].minID)
        self.assertEqual(1, multiRel1.centralSubconstituent[0].maxID)
        self.assertEqual(True, multiRel1.centralSubconstituent[0].isNuclear)
        self.assertEqual(True, multiRel1.centralSubconstituent[0].isLeaf)
        self.assertEqual(3, multiRel1.centralSubconstituent[1].minID)
        self.assertEqual(3, multiRel1.centralSubconstituent[1].maxID)
        self.assertEqual(True, multiRel1.centralSubconstituent[1].isNuclear)
        self.assertEqual(True, multiRel1.centralSubconstituent[1].isLeaf)
        self.assertEqual(4, multiRel1.centralSubconstituent[2].minID)
        self.assertEqual(4, multiRel1.centralSubconstituent[2].maxID)
        self.assertEqual(True, multiRel1.centralSubconstituent[2].isNuclear)
        self.assertEqual(True, multiRel1.centralSubconstituent[2].isLeaf)

        self.assertEqual(1, multiRel1.constituent.minID)
        self.assertEqual(2, multiRel1.constituent.maxID)
        self.assertEqual(True, multiRel1.constituent.isNuclear)
        self.assertEqual(False, multiRel1.constituent.isLeaf)
        self.assertEqual(3, multiRel1.attachmentPoint.minID)
        self.assertEqual(4, multiRel1.attachmentPoint.maxID)
        self.assertEqual(True, multiRel1.attachmentPoint.isNuclear)
        self.assertEqual(False, multiRel1.attachmentPoint.isLeaf)

        multiRel2: Relation = resultTable.get(2)
        self.assertEqual("multi", multiRel2.name)
        self.assertEqual(True, multiRel2.isMultiNuclear)
        self.assertEqual(2, len(multiRel2.centralSubconstituent))

        self.assertEqual(3, multiRel2.centralSubconstituent[0].minID)
        self.assertEqual(3, multiRel2.centralSubconstituent[0].maxID)
        self.assertEqual(True, multiRel2.centralSubconstituent[0].isNuclear)
        self.assertEqual(True, multiRel2.centralSubconstituent[0].isLeaf)
        self.assertEqual(4, multiRel2.centralSubconstituent[1].minID)
        self.assertEqual(4, multiRel2.centralSubconstituent[1].maxID)
        self.assertEqual(True, multiRel2.centralSubconstituent[1].isNuclear)
        self.assertEqual(True, multiRel2.centralSubconstituent[1].isLeaf)

        self.assertEqual(3, multiRel2.constituent.minID)
        self.assertEqual(3, multiRel2.constituent.maxID)
        self.assertEqual(True, multiRel2.constituent.isNuclear)
        self.assertEqual(True, multiRel2.constituent.isLeaf)
        self.assertEqual(4, multiRel2.attachmentPoint.minID)
        self.assertEqual(4, multiRel2.attachmentPoint.maxID)
        self.assertEqual(True, multiRel2.attachmentPoint.isNuclear)
        self.assertEqual(True, multiRel2.attachmentPoint.isLeaf)


class TestTableEvaluator(TestCase):
    def test_forEmptyRelTables(self):
        """ Given empty RstTables, the TableEvaluator shall return
            an empty ComparisonTable """
        # Build
        tabEval = TableEvaluator()
        emptyRelTable1 = RelTable()
        emptyRelTable2 = RelTable()
        # Operate
        compTable = tabEval.run(emptyRelTable1, emptyRelTable2)
        # Check
        self.assertIsInstance(compTable, ComparisonTable)
        self.assertEqual(compTable.length(), 0)

    @skip("")
    def test_comparisons(self):
        self.fail("TODO: Implement test cases for table comparisons")

    @skip("")
    def test_kappaCalculations(self):
        self.fail("TODO: Implement test cases for kappa calculations")
