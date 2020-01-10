from Ignore.element import Element
from abc import abstractmethod

class AbstractArray(object):
    @abstractmethod
    def getElement(self, index:int):
        pass
    @abstractmethod
    def setElement(self, index:int, element:Element):
        pass
    @abstractmethod
    def getLength(self):
        pass


class FixedLenghtArray(AbstractArray):
    def __init__(self, length:int):
        self.LENGTH = length
        self._elements = length * [self.LENGTH]

    def getElement(self, index:int):
        return self._elements[index]

    def setElement(self, index:int, element:Element):
        self._elements[index] = element

    def getLength(self):
        return self.LENGTH

class VariableLengthArray(AbstractArray):
    def __init__(self):
        self._element = []


    def getElement(self, index:int):
        if index < 0 or index >= self.getLength():
            raise IndexError
        return self._element[index]

    def setElement(self, index:int, element:Element):
        if index < 0 or index >= self.getLength():
            raise IndexError
        self._element[index] = element

    def getLength(self):
        return len(self._element)


    def resize(self, newLength:int):
        length = self.getLength()
        if newLength < length:
            self._element = self._element[:newLength]

        elif newLength > length:
            ext = (newLength - length) * [None]
            self._element.extend(ext)

    def deleteElement(self, index):
        if index < 0 or index >= self.getlenght():
            raise IndexError

        if index == 0:
            self._element = self._element[1:]

        elif idnex == self.getLength() -1:
            self._element = self._element[:index]

        else:
            self._element = self._element[:index] + self._element[index + 1:]

x = VariableLengthArray()

print(x.getElement(2))

print(x._elements)
