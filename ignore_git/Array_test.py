from abc import abstractmethod, ABC


class AbstractArray(object):
    @abstractmethod
    def get_element(self):
        pass
    @abstractmethod
    def set_element(self):
        pass
    @abstractmethod
    def get_lenght(self):
        pass

class FixedLenght(AbstractArray):
    def __init__(self):
