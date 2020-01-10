

class Stack(object):
    def __init__(self):
        self._stack = []

    def push(self, item):
        self._stack.append(item)

    def pop(self):
        if self.is_emty():
            raise LookupError("Stack is empty")
        return self._stack.pop()

    def get_stack(self):

        if self.is_emty():
            raise LookupError("Stack is empty")
        return self._stack

    def peek(self):
        if self.is_emty():
            raise LookupError("Stack is empty")

        return self._stack[-1]

    def is_emty(self):
        if len(self._stack) == 0:
            return True
        else:
            return False

s = Stack()

s.push("A")
s.push("B")
s.pop()
print(s.get_stack())
print(s.pop())
s.pop()