from element import Element

class Stack(object):
    def __init__(self):
        self._stack = []

    def push(self, e:Element):
        self._stack.append(e)

    def pop(self):
        if self.is_empty():
            raise LookupError("Empty")
        return self._stack.pop()

    def peek(self):
        if self.is_empty():
            raise LookupError("Empty")
        return self._stack[-1]


    def is_empty(self):
        if len(self._stack) == 0:
            return True
        else:
            return False



x = Stack()
x.push(1)
x.push(2)
x.push(3)
x.push(4)
x.push(5)
x.push(6)
x.push(7)

print(x.peek())
print(x.pop())