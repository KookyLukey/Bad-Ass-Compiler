import sys
import re
from Node import Node
from LinkedList import LinkedList

class irConverter(object):

    def __init__(self, ll = None):
        self.ll = ll

    def printList(self):
        print(self.ll.returnString(0).get_instr())

    def tinyBuilder(self):
        node = self.ll.returnStart()
        while(node is not None):
            if (node.get_instr() != 'LINK'):

                if (node.get_instr() == 'STOREI'):

                    if ("$T" in node.get_op1()):
                        node.set_op1("r" + str(int(node.get_op1()[2:])-1))

                    if ("$T" in node.get_op2()):
                        temp = node.get_op2().lstrip('$T')
                        temp = int(temp) - 1
                        node.set_op2("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_op2())

                if (node.get_instr() == 'LABEL'):
                    print("label " + node.get_op1())

                if (node.get_instr() == 'JUMP'):
                    print("jmp " + node.get_op1())

                if (node.get_instr() == 'READI'):
                    print("sys readi " + node.get_op1())

                if (node.get_instr() == 'WRITEI'):
                    print("sys writei " + node.get_op1())

                if (node.get_instr() == 'WRITES'):
                    print("sys writes " + node.get_op1())

                if (node.get_instr() == 'EQI'):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    print("cmpi " + node.get_op1() + " " + node.get_op2())
                    print("jeq " + node.get_result())

                if (node.get_instr() == 'LEI'):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    print("cmpi " + node.get_op1() + " " + node.get_op2())
                    print("jle " + node.get_result())

                if (node.get_instr() == 'LEF'):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    print("cmpr " + node.get_op1() + " " + node.get_op2())
                    print("jle " + node.get_result())

                if (node.get_instr() == 'GEI'):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    print("cmpi " + node.get_op1() + " " + node.get_op2())
                    print("jge " + node.get_result())

                if (node.get_instr() == 'ADDI' and '$T' in node.get_op1() and '$T' in node.get_op2()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("addi " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'ADDI' and '$T' in node.get_op1()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("addi " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'ADDI' and '$T' in node.get_op2()):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("addi " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'ADDI'):
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("addi " + node.get_op2() + " " + node.get_result())

                if (node.get_instr() == 'SUBI' and '$T' in node.get_op1() and '$T' in node.get_op2()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("subi " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'SUBI' and '$T' in node.get_op1()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("subi " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'SUBI' and '$T' in node.get_op2()):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op2() + " " + node.get_result())
                    print("subi " + node.get_op1() + " " + node.get_result())
                elif (node.get_instr() == 'SUBI'):
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("subi " + node.get_op2() + " " + node.get_result())
                if (node.get_instr() == 'RET'):
                    print("sys halt")
                if (node.get_instr() == 'DIVF' and '$T' in node.get_op1() and '$T' in node.get_result()):
                    temp = node.get_op1().lstrip('$T')
                    node.set_op1("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("divr " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'DIVF' and '$T' in node.get_op2() and '$T' in node.get_result()):
                    temp = node.get_op2().lstrip('$T')
                    node.set_op2("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("divr " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'DIVF' and '$T' in node.get_result()):
                    temp = node.get_result().lstrip('$T')
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("divr " + node.get_op2() + " " + node.get_result())
                if (node.get_instr() == 'DIVI' and '$T' in node.get_op1() and '$T' in node.get_result()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("divi " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'DIVI' and '$T' in node.get_op2() and '$T' in node.get_result()):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("divi " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'DIVI' and '$T' in node.get_result()):
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("divi " + node.get_op2() + " " + node.get_result())
                if (node.get_instr() == 'MULTI' and '$T' in node.get_op1() and '$T' in node.get_op2() and '$T' in node.get_result()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("muli " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'MULTI' and '$T' in node.get_op1() and '$T' in node.get_result()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("muli " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'MULTI' and '$T' in node.get_op2() and '$T' in node.get_result()):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("muli " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'MULTI' and '$T' in node.get_result()):
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("muli " + node.get_op2() + " " + node.get_result())
                if (node.get_instr() == 'MULTF' and '$T' in node.get_op1() and '$T' in node.get_op2() and '$T' in node.get_result()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("mulr " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'MULTF' and '$T' in node.get_op1() and '$T' in node.get_result()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("mulr " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'MULTF' and '$T' in node.get_op2() and '$T' in node.get_result()):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("mulr " + node.get_op2() + " " + node.get_result())
                elif (node.get_instr() == 'MULTF' and '$T' in node.get_result()):
                    temp = node.get_result().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_result("r"+str(temp))
                    print("move " + node.get_op1() + " " + node.get_result())
                    print("mulr " + node.get_op2() + " " + node.get_result())

                if(node.get_instr() == 'GTI' and '$T' in node.get_op1()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    print("cmpi " + node.get_op1() + " " + node.get_op2())
                    print("jgt " + node.get_result())
                elif(node.get_instr() == 'GTI' and '$T' in node.get_op2()):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    print("cmpi " + node.get_op1() + " " + node.get_op2())
                    print("jgt " + node.get_result())

                if(node.get_instr() == 'GTF' and '$T' in node.get_op1()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    print("cmpr " + node.get_op1() + " " + node.get_op2())
                    print("jgt " + node.get_result())
                elif(node.get_instr() == 'GTF' and '$T' in node.get_op2()):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    print("cmpr " + node.get_op1() + " " + node.get_op2())
                    print("jgt " + node.get_result())

                if(node.get_instr() == 'GEI' and '$T' in node.get_op1()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    print("cmpi " + node.get_op1() + " " + node.get_op2())
                    print("jge " + node.get_result())
                elif(node.get_instr() == 'GEI' and '$T' in node.get_op2()):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    print("cmpi " + node.get_op1() + " " + node.get_op2())
                    print("jge " + node.get_result())

                if(node.get_instr() == 'GEF' and '$T' in node.get_op1()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    print("cmpr " + node.get_op1() + " " + node.get_op2())
                    print("jge " + node.get_result())
                elif(node.get_instr() == 'GEF' and '$T' in node.get_op2()):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    print("cmpr " + node.get_op1() + " " + node.get_op2())
                    print("jge " + node.get_result())

                if(node.get_instr() == 'NEI' and '$T' in node.get_op1()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    print("cmpi " + node.get_op1() + " " + node.get_op2())
                    print("jne " + node.get_result())
                elif(node.get_instr() == 'NEI' and '$T' in node.get_op2()):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    print("cmpi " + node.get_op1() + " " + node.get_op2())
                    print("jne " + node.get_result())

                if(node.get_instr() == 'NEF' and '$T' in node.get_op1()):
                    temp = node.get_op1().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op1("r"+str(temp))
                    print("cmpr " + node.get_op1() + " " + node.get_op2())
                    print("jne " + node.get_result())
                elif(node.get_instr() == 'NEF' and '$T' in node.get_op2()):
                    temp = node.get_op2().lstrip('$T')
                    temp = int(temp) - 1
                    node.set_op2("r"+str(temp))
                    print("cmpr " + node.get_op1() + " " + node.get_op2())
                    print("jne " + node.get_result())

                node = node.get_next()
            else:
                node = node.get_next()
                pass
