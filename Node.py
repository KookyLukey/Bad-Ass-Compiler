class IRN:
    def __init__(self, instr, op1, op2, result):
        self.instr = instr
        self.op1 = op1
        self.op2 = op2
        self.result = result

class Node(object):

    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node

    def set_next(self, new_next):
        self.next_node = new_next
