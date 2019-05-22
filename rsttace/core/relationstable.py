
class RelElement():
    """ Describes one of the two (or more) elements belonging to a relation """
    def __init__(self):
        self.minID: int
        self.maxID: int
        self.isNuclear: bool
        self.isLeaf: bool


class Relation():
    def __init__(self):
        self.name: str
        self.isMultiNuclear: bool
        self.constituent = RelElement()
        self.attachmentPoint = RelElement()
        self.centralSubconstituent = []


class RelTable():
    __relations: list

    def __init__(self):
        self.__relations = []

    def get(self, index: int):
        return self.__relations[index]

    def append(self, e: Relation):
        self.__relations.append(e)

    def sort(self, key):
        self.__relations.sort(key=key)

    def length(self):
        return len(self.__relations)

    def __iter__(self):
        return iter(self.__relations)

    def __add__(self, relTable):
        newTable = RelTable()
        newTable._RelTable__relations += self.__relations
        newTable._RelTable__relations += relTable._RelTable__relations
        return newTable
