import pandas as pd
from tabulate import tabulate

from rsttace.core import RelTable, Relation, RelElement
from rsttace.core import ComparisonTable, Comparison
from rsttace.core import CompareSetTable
from rsttace.core import MatchingDistance, Equivalency
from rsttace.controller import IRelTableOutput
from rsttace.controller import IComparisonTableOutput
from rsttace.controller import ICompareSetTableOutput


# RelTable outputs


class RelTableLogger(IRelTableOutput):
    def __init__(self, outputFile=""):
        self.outputFile = outputFile
        pass

    def write(self, relTable: RelTable):
        writeFile = self.__isNotEmpty(self.outputFile)
        if writeFile:
            print("\nWrite result table of RST tree analysis to: "
                  + self.outputFile)
            dataFrame = createRelationsDataframe(relTable)
            dataFrame.to_csv(self.outputFile, index=False, encoding='utf-8-sig')
            print("Output file written successfully.")

    def __isNotEmpty(self, s: str) -> bool:
        """ Checks whether string is empty or not """
        return bool(s and s.strip())


class RelTableCliOutput(IRelTableOutput):
    def write(self, relTable: RelTable):
        dataFrame = createRelationsDataframe(relTable)
        cliOutput = tabulate(dataFrame,
                             headers='keys',
                             tablefmt="rst",
                             showindex=False)

        print("\nResult table of RST tree analysis:")
        print(cliOutput)


class RelTableDummyOutput(IRelTableOutput):
    def write(self, relTable: RelTable):
        pass


# CompTable outputs


class CompTableLogger(IComparisonTableOutput):
    def __init__(self, compFile="", evalFile=""):
        self.compFile = compFile
        self.evalFile = evalFile
        pass

    def write(self, compTable: ComparisonTable):
        writeCompFile = self.__isNotEmpty(self.compFile)
        if writeCompFile:
            print("Write result table of RST tree pair comparison to: "
                  + self.compFile)
            dataFrame = createComparisonDataframe(compTable)
            dataFrame.to_csv(self.compFile, index=False, encoding='utf-8-sig')
            print("Output file written successfully.")
        writeEvalFile = self.__isNotEmpty(self.evalFile)
        if writeEvalFile:
            print("Write result metrics of RST tree pair evalarison to: "
                  + self.evalFile)
            dataFrame = createEvaluationDataframe(compTable)
            dataFrame.to_csv(self.evalFile, index=True, encoding='utf-8-sig')
            print("Output file written successfully.")

    def __isNotEmpty(self, s: str) -> bool:
        """ Checks whether string is empty or not """
        return bool(s and s.strip())


class CompTableCliOutput(IComparisonTableOutput):
    def write(self, compTable: ComparisonTable):
        # prepare tables
        compTableFrame = createComparisonDataframe(compTable)
        evalTableFrame = createEvaluationDataframe(compTable)
        compTableCli = tabulate(compTableFrame,
                                headers='keys',
                                tablefmt="rst",
                                showindex=False)
        evalTableCli = tabulate(evalTableFrame,
                                headers='keys',
                                tablefmt="rst",
                                showindex=True)

        # write on CLI
        print("\nResult table of RST tree pair comparison:")
        print(compTableCli)
        print("\nStatistical metrics:")
        print(evalTableCli)


class CompTableDummyOutput(IComparisonTableOutput):
    def write(self, compTable: ComparisonTable):
        pass


# Eval table output


class CompareSetTableLogger(ICompareSetTableOutput):
    def __init__(self, outputFile=""):
        self.outputFile = outputFile
        pass

    def write(self, compSetTable: CompareSetTable):
        writeFile = self.__isNotEmpty(self.outputFile)
        if writeFile:
            print("Write result table of RST tree pair comparison to: "
                  + self.outputFile)
            extDataFrame = self.__appendStatsToDataFrame(compSetTable)
            extDataFrame.to_csv(self.outputFile, index=False)
            print("Output file written successfully.")
        pass

    def __isNotEmpty(self, s: str) -> bool:
        """ Checks whether string is empty or not """
        return bool(s and s.strip())

    def __appendStatsToDataFrame(self, evalTable):
        # App empty row as separator:
        empty_row = pd.Series()  # This creates a Series with no data
        dataFrame = pd.concat([evalTable.dataFrame, empty_row.to_frame().T], ignore_index=True, sort=False)

        # Add statsFrame as last row to dataFrame
        statsFrame = evalTable.stats
        statsFrame["Name"] = statsFrame.index
        return pd.concat([dataFrame, statsFrame], ignore_index=True, sort=False)


class CompareSetTableCliOutput(ICompareSetTableOutput):
    def write(self, compSetTable: CompareSetTable):
        # prepare tables
        evalTableCli = tabulate(compSetTable.dataFrame,
                                headers='keys',
                                tablefmt="rst",
                                showindex=False)
        statsTableCli = tabulate(compSetTable.stats,
                                 headers='keys',
                                 tablefmt="rst",
                                 showindex=True)
        # write on CLI
        print("\nStatistical evaluation of the whole RST tree pair set:")
        print("\nResults for each RST tree pair:")
        print(evalTableCli)
        print("\nOverall results of whole dataset:")
        print(statsTableCli)
        return


class CompareSetTableDummyOutput(ICompareSetTableOutput):
    def write(self, compSetTable: CompareSetTable):
        pass


# Support functions


def createRelationsDataframe(relTable: RelTable) -> pd.DataFrame:
    labels = createRelCsvHeader()
    rows = []
    for rel in relTable:
        rows.append(createRelCsvEntry(rel))
    return pd.DataFrame.from_records(rows, columns=labels)


def createComparisonDataframe(compTable: ComparisonTable) -> pd.DataFrame:
    labels = createCompCsvHeader()
    rows = []

    biasID = 1
    for i in range(0, compTable.length()):
        comp: Comparison = compTable.get(i)
        rel1_strLst = createRelCsvEntry(comp.relation1)
        rel2_strLst = createRelCsvEntry(comp.relation2)
        match_str = createMatchingString(comp.matchingDistance)

        if comp.matchingDistance == MatchingDistance.NO_MATCHING:
            # own line for rel1
            id_str = str(i+biasID)
            csvRow = [id_str, ""] + rel1_strLst + [""] + \
                createEmptyRelCsvEntry() + ["", match_str] + \
                createEmptyEvaluation()
            rows.append(csvRow)
            # own line for rel2
            id_str = str(i+biasID+1)
            csvRow = [id_str, ""] + createEmptyRelCsvEntry() + \
                [""] + rel2_strLst + ["", match_str] + \
                createEmptyEvaluation()
            rows.append(csvRow)

            biasID += 1
        else:
            id_str = str(i+biasID)
            csvRow = [id_str, ""] + rel1_strLst + [""] + \
                rel2_strLst + ["", match_str] + \
                createEvaluationString(comp.evaluation)
            rows.append(csvRow)

    return pd.DataFrame.from_records(rows, columns=labels)


def createEvaluationDataframe(compTable: ComparisonTable) -> pd.DataFrame:
    combined = {"Matching Ratios": compTable.matchingRatios,
                "Inter Annotator Agreement": compTable.cohensKappas}
    return pd.DataFrame.from_dict(combined, 'index')


def createRelCsvHeader() -> list:
    return ["CS", "Relation", "Nuc",
            "C1", "C2", "CN",
            "A1", "A2", "AN"]


def createCompCsvHeader() -> list:
    return ["ID", "",
            "CS-A", "Relation-A", "Nuc-A",
            "C1-A", "C2-A", "CN-A",
            "A1-A", "A2-A", "AN-A",
            "",
            "CS-B", "Relation-B", "Nuc-B",
            "C1-B", "C2-B", "CN-B",
            "A1-B", "A2-B", "AN-B",
            "", "Matching",
            "N", "R", "C", "A", "Agreement", "Disagreement"]


def createRelCsvEntry(rel: Relation) -> list:
    CS_str = createStringForCentralSubconstituent(rel.centralSubconstituent)
    Rel_str = rel.name
    Nuc_str = createNuclearityString(rel)
    C1_str = str(rel.constituent.minID)
    C2_str = str(rel.constituent.maxID)
    CN_str = 'N' if rel.constituent.isNuclear else 'S'
    A1_str = str(rel.attachmentPoint.minID)
    A2_str = str(rel.attachmentPoint.maxID)
    AN_str = 'N' if rel.attachmentPoint.isNuclear else 'S'

    return [CS_str, Rel_str, Nuc_str,
            C1_str, C2_str, CN_str,
            A1_str, A2_str, AN_str]


def createEmptyRelCsvEntry() -> list:
    return ["", "", "", "", "", "", "", "", ""]


def createStringForRelElement(relElem: RelElement,
                              writeNuclearity: bool) -> str:
    if relElem.minID != relElem.maxID:
        numberStr = str(relElem.minID) + "-" + str(relElem.maxID)
    else:
        numberStr = str(relElem.minID)

    if writeNuclearity:
        if relElem.isNuclear:
            return numberStr + "N"
        else:
            return numberStr + "S"
    else:
        return numberStr


def createStringForCentralSubconstituent(relElemList: list) -> str:
    string = ""
    for i in range(0, len(relElemList)):
        relElem = relElemList[i]
        string = string + createStringForRelElement(relElem, False)
        if i < len(relElemList)-1:
            string = string + "|"
    return string


def createNuclearityString(rel: Relation) -> str:
    if rel.isMultiNuclear:
        return "⟷"
    elif rel.constituent.maxID < rel.attachmentPoint.minID:
        return "⟶"
    elif rel.constituent.minID > rel.attachmentPoint.maxID:
        return "⟵"
    else:
        return "⟷"


def createMatchingString(dist: int) -> str:
    if dist == MatchingDistance.COMPLETE_SAME_CS:
        return "Completely identical CS"
    elif dist == MatchingDistance.PARTIALLY_SAME_CS:
        return "Partially identical CS"
    elif dist == MatchingDistance.SAME_C_SAME_A:
        return "C1=C2 and A1=A2"
    elif dist == MatchingDistance.SWITCHED_C_AND_A:
        return "C1=A2 and A1=C2"
    else:
        return "No matching"


def createEmptyEvaluation() -> list:
    return ["", "", "", "", "", ""]


def createEvaluationString(eval: Equivalency) -> list:
    tick = '✓'
    noTick = '✗'
    agreement = ""
    disAgreement = ""

    if eval.nuclearity.equalDirection:
        N_str = tick
        agreement = agreement + 'N'
    else:
        N_str = noTick
        if eval.nuclearity.equalMonoMulti:
            disAgreement = disAgreement + 'N/S'
        else:
            disAgreement = disAgreement + 'N/N-N/S'

    if eval.relation:
        R_str = tick
        agreement = agreement + 'R'
    else:
        R_str = noTick
        if len(disAgreement) > 0:
            disAgreement = disAgreement + ", "
        disAgreement = disAgreement + '≠R'

    if eval.constituent:
        C_str = tick
        agreement = agreement + 'C'
    else:
        C_str = noTick

    if eval.attachmentPoint:
        A_str = tick
        agreement = agreement + 'A'
    else:
        A_str = noTick

    return [N_str, R_str, C_str, A_str, agreement, disAgreement]
