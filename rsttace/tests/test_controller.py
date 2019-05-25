from unittest import TestCase

from rsttace.controller.interactors import AnalyseInteractor
from rsttace.controller.interactors import CompareInteractor
from rsttace.controller.interactors import EvaluateInteractor
from rsttace.controller import IRstInput
from rsttace.controller import IRelTableOutput
from rsttace.controller import IComparisonTableOutput
from rsttace.controller import IEvaluationTableOutput
from rsttace.core import RstTree
from rsttace.core import RelTable, ComparisonTable, EvaluationTable


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

    def write(self, compTable: ComparisonTable):
        self.write_timesCalled += 1


class FakeEvalTableOutput(IEvaluationTableOutput):
    def __init__(self):
        self.write_timesCalled = 0

    def write(self, evalTable: EvaluationTable):
        self.write_timesCalled += 1


class FakeGenerator():
    def __init__(self):
        self.run_timesCalled = 0

    def run(self, rstTree: RstTree):
        self.run_timesCalled += 1
        return RelTable()


class FakeComparer():
    def __init__(self):
        self.run_timesCalled = 0

    def run(self,
            relTable1: RelTable,
            relTable2: RelTable) -> ComparisonTable:
        self.run_timesCalled += 1
        return ComparisonTable()


class FakeEvaluator():
    def __init__(self):
        self.run_timesCalled = 0

    def run(self, compTables: list) -> EvaluationTable:
        self.run_timesCalled += 1
        return EvaluationTable(None)


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
        interactor.tableComparer = FakeComparer()

        interactor.run()

        self.assertEqual(rstInput1.read_timesCalled, 1)
        self.assertEqual(rstInput2.read_timesCalled, 1)
        self.assertEqual(interactor.tableComparer.run_timesCalled, 1)
        self.assertEqual(compOutput.write_timesCalled, 1)

    def test_numberOfCalls_twoOutputs(self):
        rstInput1 = FakeInput()
        rstInput2 = FakeInput()
        compOutput1 = FakeCompTableOutput()
        compOutput2 = FakeCompTableOutput()
        interactor = CompareInteractor(rstInput1,
                                       rstInput2,
                                       [compOutput1, compOutput2])
        interactor.tableComparer = FakeComparer()

        interactor.run()

        self.assertEqual(rstInput1.read_timesCalled, 1)
        self.assertEqual(rstInput2.read_timesCalled, 1)
        self.assertEqual(interactor.tableComparer.run_timesCalled, 1)
        self.assertEqual(compOutput1.write_timesCalled, 1)
        self.assertEqual(compOutput2.write_timesCalled, 1)

    def test_returnsComparisonTable(self):
        rstInput1 = FakeInput()
        rstInput2 = FakeInput()
        interactor = CompareInteractor(rstInput1, rstInput2, [])

        returnVal = interactor.run()

        self.assertIsInstance(returnVal, ComparisonTable)


class TestEvaluateInteractor(TestCase):
    def test_numberOfCalls(self):
        # Build
        pair1tree1 = FakeInput()
        pair1tree2 = FakeInput()
        pair1compOut = FakeCompTableOutput()

        pair2tree1 = FakeInput()
        pair2tree2 = FakeInput()
        pair2compOut = FakeCompTableOutput()

        pair3tree1 = FakeInput()
        pair3tree2 = FakeInput()
        pair3compOut = FakeCompTableOutput()

        evalOutput1 = FakeEvalTableOutput()
        evalOutput2 = FakeEvalTableOutput()

        pair1triple = (pair1tree1, pair1tree2, pair1compOut)
        pair2triple = (pair2tree1, pair2tree2, pair2compOut)
        pair3triple = (pair3tree1, pair3tree2, pair3compOut)

        # Operate
        interactor = EvaluateInteractor([pair1triple,
                                         pair2triple,
                                         pair3triple],
                                        [evalOutput1, evalOutput2])
        interactor.tableEvaluator = FakeEvaluator()

        returnVal = interactor.run()

        # Check
        self.assertEqual(interactor.tableEvaluator.run_timesCalled, 1)
        self.assertIsInstance(returnVal, EvaluationTable)

        self.assertEqual(pair1tree1.read_timesCalled, 1)
        self.assertEqual(pair1tree2.read_timesCalled, 1)
        self.assertEqual(pair1compOut.write_timesCalled, 1)

        self.assertEqual(pair2tree1.read_timesCalled, 1)
        self.assertEqual(pair2tree2.read_timesCalled, 1)
        self.assertEqual(pair2compOut.write_timesCalled, 1)

        self.assertEqual(pair3tree1.read_timesCalled, 1)
        self.assertEqual(pair3tree2.read_timesCalled, 1)
        self.assertEqual(pair3compOut.write_timesCalled, 1)

        self.assertEqual(evalOutput1.write_timesCalled, 1)
        self.assertEqual(evalOutput2.write_timesCalled, 1)
