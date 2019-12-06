class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None

    def has_value(self, value):
        if self.data == value:
            return True
        else:
            return False


class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

        return

    def add(self, item):
        if not isinstance(item, Node):
            item = Node(item)
        if self.head is None:
            self.head = item
            item.next = None
            item.previous = None
            self.tail = item

        else:
            self.tail.next = item
            item.previous = self.tail
            self.tail = item

    def get_list(self):
        result = []
        current_node = self.head
        while current_node is not None:
            result.append(current_node.data)
            current_node = current_node.next
        return result

    def insert_after_index(self, value, index):
        node_index = 0
        current_node = self.head

        while current_node is not None:
            print(self.get_list())
            if node_index == index:
                new_node = Node(value)
                new_node.next = current_node.next
                current_node.next = new_node
                new_node.previous = current_node
                print(current_node.data)
                if new_node.next is not None:
                    new_node.next.previous = new_node
                return
            print(node_index)
            current_node = current_node.next
            node_index += 1

        pass


t = DoubleLinkedList()

for r in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    t.add(r)

print(t.get_list())

t.insert_after_index(1, 4)

print(t.get_list())
