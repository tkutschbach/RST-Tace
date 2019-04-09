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

    def __init__(self):
        self.__comparisons = []
        return

    def get(self, index: int):
        return self.__comparisons[index]

    def append(self, e: Comparison):
        self.__comparisons.append(e)

    def length(self):
        return len(self.__comparisons)

    def __iter__(self):
        return iter(self.__comparisons)
