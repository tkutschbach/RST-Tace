from unittest import TestCase
from rsttace.input import RstTreeParser, InvalidRstFile
from rsttace.core.rsttree import RstType, RstNode
from rsttace.core.rsttree import MonoNucRelation, MultiNucRelation, Span

import rsttace.input.parser as package
from os.path import join


def stub_readFile(filePath: str):
    """ Fake read file returns passed filePath """
    return filePath


def stub_fileExistsTrue(filePath: str):
    return True


def stub_fileExistsFalse(filePath: str):
    return False


class TestRstTreeParser_withStubs(TestCase):
    def setUp(self):
        self.origReadFile = package.readFile
        self.origFileExists = package.fileExists
        package.readFile = stub_readFile

    def tearDown(self):
        package.readFile = self.origReadFile
        package.fileExists = self.origFileExists

    def test_init_nonExistingFile(self):
        package.fileExists = stub_fileExistsFalse

        with self.assertRaises(FileNotFoundError):
            RstTreeParser("fakeFilePath")

    def test_init_readsFile(self):
        package.fileExists = stub_fileExistsTrue
        filePath = "<some file path>"

        parser = RstTreeParser(filePath)

        self.assertEqual(filePath, parser.fileContent)


class TestRstTreeParser_withFiles(TestCase):
    filePath = './rsttace/tests/testFiles'

    def test_read_fileWithWrontRoot(self):
        path = join(self.filePath, 'invalidFile_wrongXmlRoot.rs3')

        parser = RstTreeParser(path)
        with self.assertRaises(InvalidRstFile):
            parser.read()

    def test_read_fileWithoutBody(self):
        path = join(self.filePath, 'invalidFile_noBody.rs3')

        parser = RstTreeParser(path)
        with self.assertRaises(InvalidRstFile):
            parser.read()

    def test_read_fileWithoutHeader(self):
        path = join(self.filePath, 'invalidFile_noHeader.rs3')

        parser = RstTreeParser(path)
        with self.assertRaises(InvalidRstFile):
            parser.read()

    def test_read_fileWithInvalidTagInHeader(self):
        path = join(self.filePath, 'invalidFile_invalidTagInHeader.rs3')

        parser = RstTreeParser(path)
        with self.assertRaises(InvalidRstFile):
            parser.read()

    def test_read_fileWithInvalidTagInBody(self):
        path = join(self.filePath, 'invalidFile_invalidTagInBody.rs3')

        parser = RstTreeParser(path)
        with self.assertRaises(InvalidRstFile):
            parser.read()

    def test_read_fileWithInvalidRelation(self):
        path = join(self.filePath, 'invalidFile_invalidRelation.rs3')

        parser = RstTreeParser(path)
        with self.assertRaises(InvalidRstFile):
            parser.read()

    def test_read_fileWithSegmentWithoutText(self):
        path = join(self.filePath, 'invalidFile_segmentWithoutText.rs3')

        parser = RstTreeParser(path)
        with self.assertRaises(InvalidRstFile):
            parser.read()

    def test_read_fileWithMultipleTreeRoots(self):
        path = join(self.filePath, 'invalidFile_multipleTreeRoots.rs3')

        parser = RstTreeParser(path)
        with self.assertRaises(InvalidRstFile):
            parser.read()

    def test_read_fileWithInvalidMultiNucParent(self):
        path = join(self.filePath, 'invalidFile_parentOfMultiNucIsSegment.rs3')

        parser = RstTreeParser(path)
        with self.assertRaises(InvalidRstFile):
            parser.read()

    def test_read_fileWithWrongGroupType(self):
        path = join(self.filePath, 'invalidFile_wrongGroupType.rs3')

        parser = RstTreeParser(path)
        with self.assertRaises(InvalidRstFile):
            parser.read()

    def test_read_fileWithGroupAsLeafNode(self):
        path = join(self.filePath, 'invalidFile_groupAsLeafNode.rs3')

        parser = RstTreeParser(path)
        with self.assertRaises(InvalidRstFile):
            parser.read()

    def test_read_fileWithOnlyRelations(self):
        path = join(self.filePath, 'onlyRelations.rs3')

        parser = RstTreeParser(path)
        rstTree = parser.read()

        expectedRelations = dict({'span': RstType.SPAN,
                                  'background': RstType.MONO_NUCLEAR,
                                  'sequence': RstType.MULTI_NUCLEAR})
        self.assertEqual(expectedRelations, rstTree.relations)

    def test_read_fileWithSingleMonoNuc(self):
        path = join(self.filePath, 'singleMonoNuc.rs3')

        parser = RstTreeParser(path)
        rstTree = parser.read()

        root: RstNode = rstTree.root
        self.assertIsNotNone(root)
        self.assertIsNone(root.text)
        self.assertIsNone(root.toParent)
        self.assertIsNone(root.toSibling)
        self.assertIsInstance(root.toChildren, Span)
        self.assertEqual([1, 2], root.segmentID)

        span: Span = root.toChildren
        self.assertIsNotNone(span)
        self.assertIs(root, span.parent)
        self.assertEqual(2, len(span.children))

        segmentA: RstNode = span.children[0]
        self.assertIsInstance(segmentA, RstNode)
        self.assertIs(span, segmentA.toParent)
        self.assertIsInstance(segmentA.toSibling, MonoNucRelation)
        self.assertIsNone(segmentA.toChildren)
        self.assertEqual("A", segmentA.text)
        self.assertEqual([1], segmentA.segmentID)

        segmentB: RstNode = span.children[1]
        self.assertIsInstance(segmentB, RstNode)
        self.assertIs(span, segmentB.toParent)
        self.assertIsInstance(segmentB.toSibling, MonoNucRelation)
        self.assertIsNone(segmentB.toChildren)
        self.assertEqual("B", segmentB.text)
        self.assertEqual([2], segmentB.segmentID)

        relation: MonoNucRelation = segmentA.toSibling
        self.assertIs(relation, segmentB.toSibling)
        self.assertIs(relation.start, segmentB)
        self.assertIs(relation.end, segmentA)
        self.assertEqual("reason", relation.relation)

        self.assertEqual([relation], rstTree.monoNucs)
        self.assertEqual([], rstTree.multiNucs)

    def test_read_fileWithSingleMultiNuc(self):
        path = join(self.filePath, 'singleMultiNuc.rs3')

        parser = RstTreeParser(path)
        rstTree = parser.read()

        root: RstNode = rstTree.root
        self.assertIsInstance(root, RstNode)
        self.assertIsNone(root.text)
        self.assertIsNone(root.toParent)
        self.assertIsNone(root.toSibling)
        self.assertIsInstance(root.toChildren, MultiNucRelation)
        self.assertEqual([1, 3], root.segmentID)

        multiNuc: MultiNucRelation = root.toChildren
        self.assertIsNotNone(multiNuc)
        self.assertIs(root, multiNuc.parent)
        self.assertEqual(3, len(multiNuc.children))

        segmentA: RstNode = multiNuc.children[0]
        self.assertIsInstance(segmentA, RstNode)
        self.assertIs(multiNuc, segmentA.toParent)
        self.assertIsNone(segmentA.toSibling)
        self.assertIsNone(segmentA.toChildren)
        self.assertEqual("A", segmentA.text)
        self.assertEqual([1], segmentA.segmentID)

        segmentB: RstNode = multiNuc.children[1]
        self.assertIsInstance(segmentB, RstNode)
        self.assertIs(multiNuc, segmentB.toParent)
        self.assertIsNone(segmentB.toSibling)
        self.assertIsNone(segmentB.toChildren)
        self.assertEqual("B", segmentB.text)
        self.assertEqual([2], segmentB.segmentID)

        segmentC: RstNode = multiNuc.children[2]
        self.assertIsInstance(segmentC, RstNode)
        self.assertIs(multiNuc, segmentC.toParent)
        self.assertIsNone(segmentC.toSibling)
        self.assertIsNone(segmentC.toChildren)
        self.assertEqual("C", segmentC.text)
        self.assertEqual([3], segmentC.segmentID)

        self.assertEqual([], rstTree.monoNucs)
        self.assertEqual([multiNuc], rstTree.multiNucs)

    def test_read_fileWithMultiAndMonoNuc(self):
        path = join(self.filePath, 'multiAndMonoNuc.rs3')

        parser = RstTreeParser(path)
        rstTree = parser.read()

        root: RstNode = rstTree.root
        self.assertIsInstance(root, RstNode)
        self.assertIsNone(root.text)
        self.assertIsNone(root.toParent)
        self.assertIsInstance(root.toSibling, MonoNucRelation)
        self.assertIsInstance(root.toChildren, MultiNucRelation)
        self.assertEqual([1, 3], root.segmentID)

        monoNuc: MonoNucRelation = root.toSibling
        self.assertIsNotNone(monoNuc)
        self.assertIs(root, monoNuc.end)
        self.assertIsInstance(monoNuc.start, RstNode)

        multiNuc: MultiNucRelation = root.toChildren
        self.assertIsNotNone(multiNuc)
        self.assertIs(root, multiNuc.parent)
        self.assertEqual(3, len(multiNuc.children))

        self.assertEqual([monoNuc], rstTree.monoNucs)
        self.assertEqual([multiNuc], rstTree.multiNucs)

        segmentA: RstNode = multiNuc.children[0]
        self.assertIsInstance(segmentA, RstNode)
        self.assertIs(multiNuc, segmentA.toParent)
        self.assertIsNone(segmentA.toSibling)
        self.assertIsNone(segmentA.toChildren)
        self.assertEqual("A", segmentA.text)
        self.assertEqual([1], segmentA.segmentID)

        segmentB: RstNode = multiNuc.children[1]
        self.assertIsInstance(segmentB, RstNode)
        self.assertIs(multiNuc, segmentB.toParent)
        self.assertIsNone(segmentB.toSibling)
        self.assertIsNone(segmentB.toChildren)
        self.assertEqual("B", segmentB.text)
        self.assertEqual([2], segmentB.segmentID)

        segmentC: RstNode = multiNuc.children[2]
        self.assertIsInstance(segmentC, RstNode)
        self.assertIs(multiNuc, segmentC.toParent)
        self.assertIsNone(segmentC.toSibling)
        self.assertIsNone(segmentC.toChildren)
        self.assertEqual("C", segmentC.text)
        self.assertEqual([3], segmentC.segmentID)

        segmentD: RstNode = monoNuc.start
        self.assertIsNone(segmentD.toParent)
        self.assertIs(monoNuc, segmentD.toSibling)
        self.assertIsNone(segmentD.toChildren)
        self.assertEqual("D", segmentD.text)
        self.assertEqual([4], segmentD.segmentID)
