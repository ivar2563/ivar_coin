import random

class Stack(object):
    def __init__(self):
        self.stack = []

    def add(self, length):
        if length == 0:
            pass
        else:
            for num in range(length):
                num += 1
                self.stack.append(str(num))

    def pop(self, length):
        if length == 0:
            pass
        if self.is_empty():
            raise LookupError("There is no stack")
        for num in range(length):
            self.stack.pop()

    def pop_and_return(self):
        if self.is_empty():
            raise LookupError("There is no stack")
        return self.stack.pop()

    def get(self, index):
        if self.is_empty():
            raise LookupError("There is no stack")
        if index >= len(self.stack):
            pass
        else:
            while True:
                index_value = self.stack.pop()
                if len(self.stack) == index:
                    return index_value

    def remove(self, from_index, to_index):
        if self.is_empty():
            raise LookupError("There is no stack")
            pass
        temp_stack = []
        if True:
            x = 0
            while x == 0:
                temp_stack.append(self.stack.pop())
                if to_index == len(self.stack):
                    x += 1
        if True:
            x = 0
            while x == 0:
                self.stack.pop()
                if from_index == len(self.stack):
                    x += 1
        if True:
            x = 0
            while x == 0:
                self.stack.append(temp_stack.pop())
                if len(temp_stack) == 0:
                    x += 1

    def get_stack(self):
        if self.is_empty():
            raise LookupError("There is no stack")
        else:
            return self.stack

    def is_empty(self):
        if len(self.stack) == 0:
            return True
        else:
            return False


s = Stack()
s.add(200)
print(s.get_stack())
s.remove(0, 100)
print(s.get_stack())
