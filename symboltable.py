increment = 1
symbolTableInUse = ""
err = False

symbolTable = {}
stack = []
mainGlobal = []

def stopBlock():
    symbolTable.pop(stack.pop())

def decl(name,type,value):
    if (value):
        pushToTable(name, "STRING", symbolTableInUse,value)
        mainGlobal.append("name " + name + " type STRING value " + value)
    else:
        pushToTable(name, type, symbolTableInUse, 0)
        mainGlobal.append("name " + name + " type " + type)

def startFunc(name):
    stack.append(name)
    global symbolTableInUse
    symbolTableInUse = name
    symbolTable[name] = {}
    if symbolTableInUse != "GLOBAL":
        mainGlobal.append("")
    mainGlobal.append("Symbol table " + symbolTableInUse)

def stopFunc():
    symbolTable.pop(stack.pop())

def startBlock():
    global increment
    name = "BLOCK " + str(increment)
    stack.append(name)
    increment += 1
    global symbolTableInUse
    symbolTableInUse = name
    symbolTable[symbolTableInUse] = {}
    mainGlobal.append("")
    mainGlobal.append("Symbol table " + symbolTableInUse)

def pushToTable(name,type,scope,value):
    global err
    if symbolTable[scope].__contains__(name):
        if err == False:
            print("DECLARATION ERROR " + str(name))
            err = True
    else:
        symbolTable[scope][name] = {
            name: {
                "name": name,
                "type": type,
                "value": value
            }
        }

def printSymbolTablez():
    if err:
        pass
    else:
        for item in mainGlobal:
            print(item)
