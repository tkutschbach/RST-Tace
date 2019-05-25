from .evaluationtable import EvaluationTable

import pandas as pd


class TableEvaluator:
    def __init__(self):
        return

    def run(self, compTables: list) -> EvaluationTable:
        nameList = []
        nucF1List = []
        nucKappaList = []
        relF1List = []
        relKappaList = []
        conF1List = []
        conKappaList = []
        attF1List = []
        attKappaList = []

        for compTable in compTables:
            ratios = compTable.matchingRatios
            kappas = compTable.cohensKappas
            nameList.append("TODO")
            nucF1List.append(ratios["Nuclearity"])
            nucKappaList.append(kappas["Nuclearity"])
            relF1List.append(ratios["Relation"])
            relKappaList.append(kappas["Relation"])
            conF1List.append(ratios["Constituent"])
            conKappaList.append(kappas["Constituent"])
            attF1List.append(ratios["Attachment point"])
            attKappaList.append(kappas["Attachment point"])

        df = pd.DataFrame({"Name": nameList,
                           "Nuc-F1": nucF1List,
                           "Nuc-Kappa": nucKappaList,
                           "Rel-F1": relF1List,
                           "Rel-Kappa": relKappaList,
                           "Con-F1": conF1List,
                           "Con-Kappa": conKappaList,
                           "Att-F1": attF1List,
                           "Att-Kappa": attKappaList})
        return EvaluationTable(df)
