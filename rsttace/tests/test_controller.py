from unittest import TestCase

from rsttace.controller.interactors import AnalyseInteractor, CompareInteractor
from rsttace.controller import IRstInput
from rsttace.controller import IRelTableOutput, IComparisonTableOutput
from rsttace.core import RstTree
from rsttace.core import RelTable, ComparisonTable


class FakeInput(IRstInput):
    def __init__(self):
        self.read_timesCalled = 0

    def read(self) -> RstTree:
        self.read_timesCalled += 1
        return RstTree({}, None, [], [])


class FakeRelTableOutput(IRelTableOutput):
    def __init__(self):
        self.write_timesCalled = 0

    def write(self, relTable: RelTable):
        self.write_timesCalled += 1


class FakeCompTableOutput(IComparisonTableOutput):
    def __init__(self):
        self.write_timesCalled = 0

    def write(self, relTable: RelTable):
        self.write_timesCalled += 1


class FakeGenerator():
    def __init__(self):
        self.run_timesCalled = 0

    def run(self, rstTree: RstTree):
        self.run_timesCalled += 1
        return RelTable()


class FakeEvaluator():
    def __init__(self):
        self.run_timesCalled = 0

    def run(self,
            relTable1: RelTable,
            relTable2: RelTable) -> ComparisonTable:
        self.run_timesCalled += 1
        return ComparisonTable()


class TestAnalyseInteractor(TestCase):
    def test_numberOfCalls_noOutput(self):
        rstInput = FakeInput()
        interactor = AnalyseInteractor(rstInput, [])
        interactor.tableGenerator = FakeGenerator()

        interactor.run()

        self.assertEqual(rstInput.read_timesCalled, 1)
        self.assertEqual(interactor.tableGenerator.run_timesCalled, 1)

    def test_numberOfCalls_oneOutput(self):
        rstInput = FakeInput()
        relOutput = FakeRelTableOutput()
        interactor = AnalyseInteractor(rstInput, [relOutput])
        interactor.tableGenerator = FakeGenerator()

        interactor.run()

        self.assertEqual(rstInput.read_timesCalled, 1)
        self.assertEqual(interactor.tableGenerator.run_timesCalled, 1)
        self.assertEqual(relOutput.write_timesCalled, 1)

    def test_numberOfCalls_twoOutputs(self):
        rstInput = FakeInput()
        relOutput1 = FakeRelTableOutput()
        relOutput2 = FakeRelTableOutput()
        interactor = AnalyseInteractor(rstInput, [relOutput1, relOutput2])
        interactor.tableGenerator = FakeGenerator()

        interactor.run()

        self.assertEqual(rstInput.read_timesCalled, 1)
        self.assertEqual(interactor.tableGenerator.run_timesCalled, 1)
        self.assertEqual(relOutput1.write_timesCalled, 1)
        self.assertEqual(relOutput2.write_timesCalled, 1)

    def test_returnsRelationsTable(self):
        rstInput = FakeInput()
        interactor = AnalyseInteractor(rstInput, [])

        returnVal = interactor.run()

        self.assertIsInstance(returnVal, RelTable)


class TestCompareInteractor(TestCase):
    def test_numberOfCalls_noOutput(self):
        rstInput1 = FakeInput()
        rstInput2 = FakeInput()
        interactor = CompareInteractor(rstInput1, rstInput2, [])

        interactor.run()

        self.assertEqual(rstInput1.read_timesCalled, 1)
        self.assertEqual(rstInput2.read_timesCalled, 1)

    def test_numberOfCalls_oneOutput(self):
        rstInput1 = FakeInput()
        rstInput2 = FakeInput()
        compOutput = FakeCompTableOutput()
        interactor = CompareInteractor(rstInput1, rstInput2, [compOutput])
        interactor.tableEvaluator = FakeEvaluator()

        interactor.run()

        self.assertEqual(rstInput1.read_timesCalled, 1)
        self.assertEqual(rstInput2.read_timesCalled, 1)
        self.assertEqual(interactor.tableEvaluator.run_timesCalled, 1)
        self.assertEqual(compOutput.write_timesCalled, 1)

    def test_numberOfCalls_twoOutputs(self):
        rstInput1 = FakeInput()
        rstInput2 = FakeInput()
        compOutput1 = FakeCompTableOutput()
        compOutput2 = FakeCompTableOutput()
        interactor = CompareInteractor(rstInput1,
                                       rstInput2,
                                       [compOutput1, compOutput2])
        interactor.tableEvaluator = FakeEvaluator()

        interactor.run()

        self.assertEqual(rstInput1.read_timesCalled, 1)
        self.assertEqual(rstInput2.read_timesCalled, 1)
        self.assertEqual(interactor.tableEvaluator.run_timesCalled, 1)
        self.assertEqual(compOutput1.write_timesCalled, 1)
        self.assertEqual(compOutput2.write_timesCalled, 1)

    def test_returnsComparisonTable(self):
        rstInput1 = FakeInput()
        rstInput2 = FakeInput()
        interactor = CompareInteractor(rstInput1, rstInput2, [])

        returnVal = interactor.run()

        self.assertIsInstance(returnVal, ComparisonTable)
