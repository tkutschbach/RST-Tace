from rsttace.controller import IRstInput
from rsttace.core import TableGenerator, TableComparer, TableEvaluator


class AnalyseInteractor:
    def __init__(self,
                 rstInput: IRstInput,
                 tableOutputs: list):
        self.tableGenerator = TableGenerator()
        self.rstInput = rstInput
        self.tableOutputs = tableOutputs

    def run(self):
        rstTree = self.rstInput.read()
        relTable = self.tableGenerator.run(rstTree)
        for output in self.tableOutputs:
            output.write(relTable)
        return relTable


class CompareInteractor:
    def __init__(self,
                 rstInput1: IRstInput,
                 rstInput2: IRstInput,
                 tableOutputs: list):
        self.rstInput1 = rstInput1
        self.rstInput2 = rstInput2
        self.tableComparer = TableComparer()
        self.tableOutputs = tableOutputs

    def run(self):
        analyse1 = AnalyseInteractor(self.rstInput1, [])
        analyse2 = AnalyseInteractor(self.rstInput2, [])
        relTable1 = analyse1.run()
        relTable2 = analyse2.run()
        compTable = self.tableComparer.run(relTable1, relTable2)
        for output in self.tableOutputs:
            output.write(compTable)
        return compTable


class EvaluateInteractor:
    def __init__(self,
                 pairTripleList: list,
                 tableOutputs: list):
        self.pairTripleList = pairTripleList
        self.tableOutputs = tableOutputs
        self.tableEvaluator = TableEvaluator()

    def run(self):
        compTables = []
        for rstInput1, rstInput2, compTableOut in self.pairTripleList:
            compare = CompareInteractor(rstInput1, rstInput2, [compTableOut])
            compTable = compare.run()
            compTables.append(compTable)
        evalTable = self.tableEvaluator.run(compTables)
        for output in self.tableOutputs:
            output.write(evalTable)
        return evalTable
