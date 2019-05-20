from .comparisontable import ComparisonTable, Comparison, MatchingDistance
from .relationstable import RelTable, Relation, RelElement

from scipy.optimize import linear_sum_assignment
from numpy import array, zeros


class TableEvaluator():
    def __init__(self):
        return

    def run(self,
            relTable1: RelTable,
            relTable2: RelTable) -> ComparisonTable:
        distanceMatrix = generateDistMatrix(relTable1, relTable2)
        associationLists = self.__findBestAssociation(distanceMatrix)
        return self.__buildComparisonTable(relTable1,
                                           relTable2,
                                           associationLists,
                                           distanceMatrix)

    def __findBestAssociation(self, distanceMatrix: array) -> list:
        return linear_sum_assignment(distanceMatrix)

    def __buildComparisonTable(self,
                               relTable1: RelTable,
                               relTable2: RelTable,
                               associationLists: list,
                               distanceMatrix: array) -> ComparisonTable:
        compTable = ComparisonTable()
        relTable1_IDs: array = associationLists[0]
        relTable2_IDs: array = associationLists[1]

        for i in range(0, len(relTable1_IDs)):
            rel1_ID = relTable1_IDs[i]
            rel2_ID = relTable2_IDs[i]

            rel1 = relTable1.get(rel1_ID)
            rel2 = relTable2.get(rel2_ID)
            matchingDist = distanceMatrix[rel1_ID][rel2_ID]
            compTable.append(Comparison(rel1, rel2, matchingDist))

        compTable.runStatAnalysis()
        return compTable


# Relation comparison


def generateDistMatrix(relTable1: RelTable, relTable2: RelTable) -> array:
    length1 = relTable1.length()
    length2 = relTable2.length()
    distMatrix = zeros([length1, length2])

    for i in range(0, length1):
        for j in range(0, length2):
            distMatrix[i][j] = calcDistance(relTable1.get(i), relTable2.get(j))

    return distMatrix


def calcDistance(rel1: Relation, rel2: Relation) -> int:
    noMultinuclearRelations = (not rel1.isMultiNuclear) \
                              and (not rel2.isMultiNuclear)
    (allCsEqual, noCsEqual) = checkForEqualCS(rel1, rel2)

    if allCsEqual:
        return MatchingDistance.COMPLETE_SAME_CS
    else:
        if checkForEqualCC(rel1, rel2) and checkForEqualAA(rel1, rel2):
            return MatchingDistance.SAME_C_SAME_A
        elif checkForEqualCA(rel1, rel2) and checkForEqualAC(rel1, rel2):
            return MatchingDistance.SWITCHED_C_AND_A
        else:
            if noMultinuclearRelations:
                return MatchingDistance.NO_MATCHING
            else:
                if noCsEqual:
                    return MatchingDistance.NO_MATCHING
                else:
                    return MatchingDistance.PARTIALLY_SAME_CS


def oldCheckForEqualCS(rel1: Relation, rel2: Relation) -> bool:
    len1 = len(rel1.centralSubconstituent)
    len2 = len(rel2.centralSubconstituent)

    if len1 == len2:
        allEqual = True
        for i in range(0, len1):
            relElem1 = rel1.centralSubconstituent[i]
            relElem2 = rel2.centralSubconstituent[i]
            allEqual = allEqual and checkForEquality(relElem1, relElem2)
        return allEqual
    else:
        return False


def checkForEqualCS(rel1: Relation, rel2: Relation) -> (bool, bool):
    allEqual = True
    noneEqual = True

    # search all elements of CS 1 in CS 2
    for elem1 in rel1.centralSubconstituent:
        found = False
        for elem2 in rel2.centralSubconstituent:
            found = found or checkForEquality(elem1, elem2)
        allEqual = allEqual and found
        noneEqual = noneEqual and not found

    # search all elements of CS 2 in CS 1
    for elem2 in rel2.centralSubconstituent:
        found = False
        for elem1 in rel1.centralSubconstituent:
            found = found or checkForEquality(elem2, elem1)
        allEqual = allEqual and found
        noneEqual = noneEqual and not found

    return (allEqual, noneEqual)


def checkForEqualCC(rel1: Relation, rel2: Relation) -> bool:
    return checkForEquality(rel1.constituent, rel2.constituent)


def checkForEqualAA(rel1: Relation, rel2: Relation) -> bool:
    return checkForEquality(rel1.attachmentPoint, rel2.attachmentPoint)


def checkForEqualCA(rel1: Relation, rel2: Relation) -> bool:
    return checkForEquality(rel1.constituent, rel2.attachmentPoint)


def checkForEqualAC(rel1: Relation, rel2: Relation) -> bool:
    return checkForEqualCA(rel2, rel1)


def checkForEquality(relElem1: RelElement, relElem2: RelElement) -> bool:
    equalMinID = (relElem1.minID == relElem2.minID)
    equalMaxID = (relElem1.maxID == relElem2.maxID)
    return equalMinID and equalMaxID
