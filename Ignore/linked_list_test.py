import random
from random_word import RandomWords


class Node:
    def __init__(self, val):
        self.data = val
        self.next = None
        return

    def has_value(self, value):
        if self.data == value:
            return True
        else:
            return False


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None


    def add_list_item(self, item):
        if not isinstance(item, Node):
            item = Node(item)

        if self.head is None:
            self.head = item

        else:
            self.tail.next = item

        self.tail = item

        return

    def get_list(self):
        current_node = self.head
        result = []
        while current_node is not None:
            result.append(current_node.data)
            current_node = current_node.next
            print(result)
        return result

    def get_length(self):
        count = 0
        current_node = self.head
        while current_node is not None:
            current_node = current_node.next
            count += 1
        return count

    def get_by_index(self, index):
        current_node = self.head
        node_index = 0
        result = []

        while current_node is not None:
            if node_index == index:
                result.append(current_node.data)

            node_index += 1
            current_node = current_node.next

        if len(result) is 0:
            raise Exception("The list is not that long")

        return result

    def prev_node(self, index):
        current_node = self.head
        current_index = 0
        while current_node is not None:
            if current_inde:
                pass

    def insert_after_index(self, value, index):
        node_index = 0
        current_node = self.head

        while current_node is not None:
            print(node_index, current_node.data)
            if node_index == index:
                new_node = Node(value)

                new_node.next = current_node.next

                current_node.next = new_node
                return
            current_node = current_node.next
            node_index += 1
            print(node_index)

    def remove_by_id(self, index):
        node_index = 0
        current_node = self.head
        last_node = None
        result = []

        while current_node is not None:
            if node_index == index:
                result.append(current_node.data)

                pass


x = Node

node1 = x(111)
node2 = x(222)
node3 = x(333)
node4 = x(444)

abc_ = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z', 'æ', 'ø', 'å']
t = LinkedList()
temp_list = []

for a in range(100):
    temp_string = ""

    ran_int = random.randint(2, 12)
    for num in range(ran_int):
        r = random.randint(0, 26)
        temp_string += abc_[r]
    temp_list.append(temp_string)

x = [node1, node2, node3, node4]

for current_item in temp_list:
    t.add_list_item(current_item)
t.insert_after_index("Norge", 40)
#print(t.get_by_index(10))
#print(t.get_length())
#print(t.get_by_index(49))
#print(t.get_length())
print(t.get_list())


def check():
    if "Norge" in t.get_list():
        print("JAA")
    else:
        print("nei")


check()
