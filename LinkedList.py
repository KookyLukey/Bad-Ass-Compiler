from Node import Node

class LinkedList(object):

    def __init__(self, head=None, start=None):
        self.head = head
        self.start = start

    def insert(self, instr, op1, op2, result):
        if (self.start is None and self.head is None):
            new_node = Node(instr, op1, op2, result)
            self.start = new_node
        elif (self.start is not None and self.head is None):
            new_node = Node(instr, op1, op2, result)
            self.head = new_node
            self.start.set_next(self.head)
        else :
            new_node = Node(instr, op1, op2, result)
            self.head.set_next(new_node)
            self.head = new_node

    def size(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.get_next()
        return count

    def search(self, data):
        current = self.head
        found = False
        while current and found is False:
            if current.get_data() == data:
                found = True
            else:
                current = current.get_next()
        if current is None:
            raise ValueError("Data not in list")
        return current

    def printList(self):
        current = self.start
        while current is not None:
            print(current.get_instr() + " " +  current.get_op1() + " " + current.get_op2() + " " +  current.get_result())
            current = current.get_next()
