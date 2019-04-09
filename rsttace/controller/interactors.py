from rsttace.controller import IRstInput
from rsttace.core import TableGenerator, TableEvaluator


class AnalyseInteractor():
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
        self.tableEvaluator = TableEvaluator()
        self.tableOutputs = tableOutputs

    def run(self):
        analyse1 = AnalyseInteractor(self.rstInput1, [])
        analyse2 = AnalyseInteractor(self.rstInput2, [])
        relTable1 = analyse1.run()
        relTable2 = analyse2.run()
        compTable = self.tableEvaluator.run(relTable1, relTable2)
        for output in self.tableOutputs:
            output.write(compTable)
        return compTable
