import sys
import Node

def openf(file):
    irList = []
    with open(file) as f:
        lines = f.readlines()
        temp = lines.split()
        node = buildIr(temp)
        if node is not None:
            irList.append(node)

    return irList

def buildIr(list):
    if list[0] != "LABEL" && list[0] != "LINK":
        instr = list[0]

        try:
            op1 = list[1]
        except IndexError:
            op1 = ""

        try:
            op2 = list[2]
        except IndexError:
            op2 = ""

        try:
            result = list[3]
        except IndexError:
            result = ""

    else:
        pass

    return Node.IRN(instr, op1, op2, result)
