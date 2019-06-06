from .comparesettable import CompareSetTable

import pandas as pd


class TableSetComparer:
    def __init__(self):
        return

    def run(self, compTables: list) -> CompareSetTable:
        # create data lists
        nameList = []
        nucF1List = []
        nucKappaList = []
        relF1List = []
        relKappaList = []
        conF1List = []
        conKappaList = []
        attF1List = []
        attKappaList = []
        averageF1List = []
        averageKappaList = []
        for compTable in compTables:
            ratios = compTable.matchingRatios
            kappas = compTable.cohensKappas
            nameList.append(compTable.name)
            nucF1List.append(ratios["Nuclearity"])
            nucKappaList.append(kappas["Nuclearity"])
            relF1List.append(ratios["Relation"])
            relKappaList.append(kappas["Relation"])
            conF1List.append(ratios["Constituent"])
            conKappaList.append(kappas["Constituent"])
            attF1List.append(ratios["Attachment point"])
            attKappaList.append(kappas["Attachment point"])
            averageF1List.append(ratios["Average"])
            averageKappaList.append(kappas["Average"])

        # generate dataframe
        df = pd.DataFrame({"Name": nameList,
                           "Nuclearity-Ratio": nucF1List,
                           "Nuclearity-Kappa": nucKappaList,
                           "Relation-Ratio": relF1List,
                           "Relation-Kappa": relKappaList,
                           "Constituent-Ratio": conF1List,
                           "Constituent-Kappa": conKappaList,
                           "AttachmentPoint-Ratio": attF1List,
                           "AttachmentPoint-Kappa": attKappaList,
                           "Average-Ratio": averageF1List,
                           "Average-Kappa": averageKappaList})

        return CompareSetTable(df)
