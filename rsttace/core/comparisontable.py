from .relationstable import Relation, RelElement
from enum import IntEnum


class MatchingDistance(IntEnum):
    COMPLETE_SAME_CS = 0
    SAME_C_SAME_A = 1
    SWITCHED_C_AND_A = 2
    PARTIALLY_SAME_CS = 3
    NO_MATCHING = 4


class NuclearityEquivalency:
    equalDirection: bool
    equalMonoMulti: bool


class Equivalency():
    nuclearity: NuclearityEquivalency
    relation: bool
    constituent: bool
    attachmentPoint: bool


class Comparison():
    """ Describes the comparison of two RST-relations """
    relation1: Relation
    relation2: Relation
    matchingDistance: int
    evaluation: Equivalency

    def __init__(self, rel1: Relation, rel2: Relation, dist: int):
        self.relation1 = rel1
        self.relation2 = rel2
        self.matchingDistance = dist
        self.evaluation = self.__calcEquivalency()

    def __calcEquivalency(self) -> Equivalency:
        evaluation = Equivalency()
        evaluation.relation = self.__compareRelations()
        evaluation.attachmentPoint = self.__compareAttachmentPoint()
        evaluation.constituent = self.__compareConstituent()
        evaluation.nuclearity = self.__compareNuclearity()
        return evaluation

    def __compareRelations(self) -> bool:
        if self.relation1.name == self.relation2.name:
            return True
        else:
            return False

    def __compareAttachmentPoint(self) -> bool:
        attP1 = self.relation1.attachmentPoint
        attP2 = self.relation2.attachmentPoint
        return self.__compareRelElem(attP1, attP2)

    def __compareConstituent(self) -> bool:
        const1 = self.relation1.constituent
        const2 = self.relation2.constituent
        return self.__compareRelElem(const1, const2)

    def __compareRelElem(self, elem1: RelElement, elem2: RelElement) -> bool:
        equalMinID = (elem1.minID == elem2.minID)
        equalMaxID = (elem1.maxID == elem2.maxID)
        equalNuc = (elem1.isNuclear == elem2.isNuclear)
        return equalMinID and equalMaxID and equalNuc

    def __compareNuclearity(self) -> NuclearityEquivalency:
        nucEquiv = NuclearityEquivalency()
        nuc1 = self.__calculateNuclearity(self.relation1)
        nuc2 = self.__calculateNuclearity(self.relation2)

        nucEquiv.equalDirection = (nuc1 == nuc2)
        nucEquiv.equalMonoMulti = (self.relation1.isMultiNuclear
                                   == self.relation2.isMultiNuclear)
        return nucEquiv

    def __calculateNuclearity(self, rel: Relation) -> int:
        if rel.isMultiNuclear:
            return 0
        elif rel.constituent.maxID < rel.attachmentPoint.minID:
            return 1
        elif rel.constituent.minID > rel.attachmentPoint.maxID:
            return 2
        else:
            return 0


class ComparisonTable():
    __comparisons: list
    matchingRatios: dict
    cohensKappas: dict
    name: str

    def __init__(self):
        self.__comparisons = []
        self.matchingRatios = {}
        self.cohensKappas = {}
        self.name = ""
        return

    def get(self, index: int):
        return self.__comparisons[index]

    def append(self, e: Comparison):
        self.__comparisons.append(e)

    def length(self):
        return len(self.__comparisons)

    def __iter__(self):
        return iter(self.__comparisons)

    def runStatAnalysis(self):
        # re-organize data structures
        labels1_rel = []
        labels1_nuc = []
        labels1_con = []
        labels1_att = []

        labels2_rel = []
        labels2_nuc = []
        labels2_con = []
        labels2_att = []

        matches_rel = int(0)
        matches_nuc = int(0)
        matches_con = int(0)
        matches_att = int(0)
        totalNum = int(0)

        for comp in self.__comparisons:
            if comp.matchingDistance != MatchingDistance.NO_MATCHING:
                labels1_rel.append(comp.relation1.name)
                labels2_rel.append(comp.relation2.name)

                labels1_nuc.append(extractNuclearityType(comp.relation1))
                labels2_nuc.append(extractNuclearityType(comp.relation2))

                labels1_con.append(extractRelElementString(comp.relation1.constituent))
                labels2_con.append(extractRelElementString(comp.relation2.constituent))

                labels1_att.append(extractRelElementString(comp.relation1.attachmentPoint))
                labels2_att.append(extractRelElementString(comp.relation2.attachmentPoint))

                matches_rel += 1 if comp.evaluation.relation else 0
                matches_nuc += 1 if comp.evaluation.nuclearity.equalDirection and \
                                    comp.evaluation.nuclearity.equalMonoMulti else 0
                matches_con += 1 if comp.evaluation.constituent else 0
                matches_att += 1 if comp.evaluation.attachmentPoint else 0

                totalNum += 1
            else:
                labels1_rel.append(comp.relation1.name)
                labels1_rel.append("None")
                labels2_rel.append("None")
                labels2_rel.append(comp.relation2.name)

                labels1_nuc.append(extractNuclearityType(comp.relation1))
                labels1_nuc.append("None")
                labels2_nuc.append("None")
                labels2_nuc.append(extractNuclearityType(comp.relation2))

                labels1_con.append(extractRelElementString(comp.relation1.constituent))
                labels1_con.append("None")
                labels2_con.append("None")
                labels2_con.append(extractRelElementString(comp.relation2.constituent))

                labels1_att.append(extractRelElementString(comp.relation1.attachmentPoint))
                labels1_att.append("None")
                labels2_att.append("None")
                labels2_att.append(extractRelElementString(comp.relation2.attachmentPoint))

                totalNum += 2

        # calculate matching ratios
        self.matchingRatios.clear()
        self.matchingRatios["Nuclearity"] = matches_nuc / totalNum if totalNum > 0 else 0
        self.matchingRatios["Relation"] = matches_rel / totalNum if totalNum > 0 else 0
        self.matchingRatios["Constituent"] = matches_con / totalNum if totalNum > 0 else 0
        self.matchingRatios["Attachment point"] = matches_att / totalNum if totalNum > 0 else 0
        self.matchingRatios["Average"] = calcAverageOfDictValues(self.matchingRatios)

        # calculate inter annotator agreement (cohen's kappa)
        self.cohensKappas.clear()
        self.cohensKappas["Nuclearity"] = cohensKappa(labels1_nuc, labels2_nuc)
        self.cohensKappas["Relation"] = cohensKappa(labels1_rel, labels2_rel)
        self.cohensKappas["Constituent"] = cohensKappa(labels1_con, labels2_con)
        self.cohensKappas["Attachment point"] = cohensKappa(labels1_att, labels2_att)
        self.cohensKappas["Average"] = calcAverageOfDictValues(self.cohensKappas)

        return


def extractNuclearityType(rel: Relation):
    if rel.isMultiNuclear:
        return "multi"
    else:
        if rel.constituent.maxID < rel.attachmentPoint.minID:
            return "right"
        else:
            return "left"


def extractRelElementString(elem: RelElement):
    return str(elem.minID) + "-" + str(elem.maxID)


def calcAverageOfDictValues(d: dict):
    avgValue = 0.
    for value in d.values():
        avgValue += value
    avgValue /= len(d)
    return avgValue


def cohensKappa(labels1: list, labels2: list):
    from sklearn.metrics import cohen_kappa_score
    return cohen_kappa_score(labels1, labels2)
