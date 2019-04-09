# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 14:46:59 2018

@author: tinokuba
"""

from unittest import TestCase
import rsttace.commandline as comline


class TestFolderProcessing(TestCase):
    actualNumberOfCalls: int
    fakeFileList: list

    def setUp(self):
        """ Set up function stubs """
        self.origEvalFunction = comline.evaluateAndCompareForSingleFile
        self.origListDir = comline.listDirectory
        comline.evaluateAndCompareForSingleFile = self.stub_evalFunction
        comline.listDirectory = self.stub_listDir

    def tearDown(self):
        """ Reset function pointers to original """
        comline.evaluateAndCompareForSingleFile = self.origEvalFunction
        comline.listDirectory = self.origListDir

    def test_run_ignoresNonRs3Files(self):
        # Build
        self.actualNumberOfCalls = 0
        self.fakeFileList = ["nonRs3File.else",
                             "phantomFile1.rs3",
                             "phantomFile2.rs3"]
        expectedNumberOfCalls = 2
        # Operate
        comline.evaluateAndCompareTwoFolders("", "", "")
        # Check
        self.assertEqual(expectedNumberOfCalls, self.actualNumberOfCalls)

    def test_run_doesNothingForEmptyFolder(self):
        # Build
        self.actualNumberOfCalls = 0
        self.fakeFileList = []
        expectedNumberOfCalls = 0
        # Operate
        comline.evaluateAndCompareTwoFolders("", "", "")
        # Check
        self.assertEqual(expectedNumberOfCalls, self.actualNumberOfCalls)

    def stub_evalFunction(self, a, b, c, d, e):
        self.actualNumberOfCalls += 1

    def stub_listDir(self, path: str):
        return self.fakeFileList


class TestArgumentProcessing(TestCase):
    isFile: bool
    isDirectory: bool

    def setUp(self):
        """ Set up function stubs """
        self.origSingleFileCompare = comline.evaluateAndCompareForSingleFile
        self.origFolderCompare = comline.evaluateAndCompareTwoFolders
        self.origIsFile = comline.isFile
        self.origIsDirectory = comline.isDirectory
        comline.evaluateAndCompareForSingleFile = self.mock_singleFile
        comline.evaluateAndCompareTwoFolders = self.mock_twoFolders
        comline.isFile = self.stub_isFile
        comline.isDirectory = self.stub_isDirectory

    def tearDown(self):
        """ Reset function pointers to original """
        comline.evaluateAndCompareForSingleFile = self.origSingleFileCompare
        comline.evaluateAndCompareTwoFolders = self.origFolderCompare
        comline.isFile = self.origIsFile
        comline.isDirectory = self.origIsDirectory

    def test_main_noArguments(self):
        """ Test for call of main without arguments """
        # Build
        self.isFile = False
        self.isDirectory = True
        self.expected_inA = "./input/A"
        self.expected_inB = "./input/B"
        self.expected_out = "./output"
        # Operate & Check
        with self.assertRaises(self.MockTwoFoldersCalled):
            comline.mainOld()

    def test_main_singleFileNoOutput(self):
        """ Test for single file without output files """
        # Build
        inputFileA = "someFolder/fake.rs3"
        inputFileB = "otherFolder/alsofake.rs3"
        self.isFile = True
        self.isDirectory = False
        self.expected_inA = inputFileA
        self.expected_inB = inputFileB
        self.expected_outRelA = ""
        self.expected_outRelB = ""
        self.expected_outComp = ""
        # Operate & Check
        with self.assertRaises(self.MockSingleFolderCalled):
            comline.mainOld(inputFileA, inputFileB)

    def test_main_singleFileCompTableOutput(self):
        """ Test for single file without output files """
        # Build
        inputFileA = "someFolder/fake.rs3"
        inputFileB = "otherFolder/alsofake.rs3"
        outputCompTable = "againSomeFolder/fakeComp.csv"
        self.isFile = True
        self.isDirectory = False
        self.expected_inA = inputFileA
        self.expected_inB = inputFileB
        self.expected_outRelA = ""
        self.expected_outRelB = ""
        self.expected_outComp = outputCompTable
        # Operate & Check
        with self.assertRaises(self.MockSingleFolderCalled):
            comline.mainOld(inputFileA, inputFileB, outputCompTable)

    def test_main_singleFileFullOutput(self):
        """ Test for single file with full output,
            i.e. relation tables & comparison table """
        # Build
        inputFileA = "someFolder/fake.rs3"
        inputFileB = "otherFolder/alsofake.rs3"
        outputCompTable = "againSomeFolder/fakeComp.csv"
        outputRelA = "adf/relTableA.csv"
        outputRelB = "a23/relTableB.csv"
        self.isFile = True
        self.isDirectory = False
        self.expected_inA = inputFileA
        self.expected_inB = inputFileB
        self.expected_outRelA = outputRelA
        self.expected_outRelB = outputRelB
        self.expected_outComp = outputCompTable
        # Operate & Check
        with self.assertRaises(self.MockSingleFolderCalled):
            comline.mainOld(inputFileA,
                            inputFileB,
                            outputCompTable,
                            outputRelA,
                            outputRelB)

    def test_main_neitherFileNorDirectory(self):
        """ Test for invalid input paths """
        # Build
        inputFileA = "someStuff"
        inputFileB = "otherStuff"
        self.isFile = False
        self.isDirectory = False
        # Operate & Check
        with self.assertRaises(TypeError):
            comline.mainOld(inputFileA, inputFileB)

    def stub_isFile(self, path: str):
        return self.isFile

    def stub_isDirectory(self, path: str):
        return self.isDirectory

    def mock_singleFile(self, inA, inB, outRelA, outRelB, outComp):
        self.assertEqual(inA, self.expected_inA)
        self.assertEqual(inB, self.expected_inB)
        self.assertEqual(outRelA, self.expected_outRelA)
        self.assertEqual(outRelB, self.expected_outRelB)
        self.assertEqual(outComp, self.expected_outComp)
        raise self.MockSingleFolderCalled

    def mock_twoFolders(self, inA, inB, out):
        self.assertEqual(inA, self.expected_inA)
        self.assertEqual(inB, self.expected_inB)
        self.assertEqual(out, self.expected_out)
        raise self.MockTwoFoldersCalled

    class MockSingleFolderCalled(Exception):
        pass

    class MockTwoFoldersCalled(Exception):
        pass
