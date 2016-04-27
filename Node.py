class Node(object):

    def __init__(self, instr=None, op1=None, op2=None, result=None, next_node=None):
        self.instr = instr
        self.op1 = op1
        self.op2 = op2
        self.result = result
        self.next_node = next_node

    def get_instr(self):
        return self.instr

    def get_op1(self):
        return self.op1

    def get_op2(self):
        return self.op2

    def get_result(self):
        return self.result

    def get_next(self):
        return self.next_node

    def set_next(self, new_next):
        self.next_node = new_next
