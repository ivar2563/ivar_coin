from abc import abstractmethod
import random
element = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


class AbstractArray(object):

    @abstractmethod
    def getElement(self, index):
        pass
    @abstractmethod
    def setElement(self, index, element):
        pass
    @abstractmethod
    def getLength(self):
        pass




class FixedLenghtArray(AbstractArray):
    def __init__(self, length):
        self.LENGTH = length
        self._elements = length * [self.LENGTH]

    def setElement(self, index: int, element):
        self._elements[index] = element

    def getElement(self, index):
        return self._elements[index]

    def getLength(self):
        return len(self._elements)




class VariableLenghtArray(AbstractArray):
    def __init__(self):
        self._element = []

    def setElement(self, index, element):
        self._element[index] = element

    def getElement(self, index):
        return self._element[index]

    def getLength(self):
        return len(self._element)

    def resize(self, len):
        self._element = self,element[:len]

    def deleteElement(self, index):
        


f = FixedLenghtArray(11)
f.setElement(-1, 69)

print(f.getElement(-1))