import sys

def openf(file):
    irList = []
    with open(file) as f:
        lines = f.readlines()
        temp = lines.split()
        node = buildIr(temp)
        if node is not None:
            irList.extend(node)

    return irList

def buildIr(list):
    if list[0] != "LABEL" && list[0] != "LINK":

    else:
        pass

    return
