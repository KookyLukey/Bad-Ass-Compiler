increment = 1
symbolTableInUse = ""
err = False

symbolTable = {}
stack = []
mainGlobal = []

def decl(name,type,value):
    if (value):
        pushToTable(name, "STRING", symbolTableInUse,value)
        mainGlobal.append("name " + name + " type STRING value " + value)
#    if (type(value) is int):
#        pushToTable(name, type, symbolTableInUse, value)
    else:
        pushToTable(name, type, symbolTableInUse, 0)
        mainGlobal.append("name " + name + " type " + type)

def mGlobal(name):
    if(name):
        global symbolTableInUse
        stack.append(name)
        symbolTableInUse = name
        symbolTable[symbolTableInUse] = {}
        if symbolTableInUse != "GLOBAL":
            mainGlobal.append("")
        mainGlobal.append("Symbol table " + symbolTableInUse)
#    else:
#        symbolTable.pop(stack.pop())

def block(num):
    if(num == 1):
        global increment
        global symbolTableInUse
        name = "BLOCK " + str(increment)
        stack.append(name)
        increment += 1
        symbolTableInUse = name
        symbolTable[symbolTableInUse] = {}
        mainGlobal.append("")
        mainGlobal.append("Symbol table " + symbolTableInUse)
#    else:
#        symbolTable.pop(stack.pop())

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

def checkType(name):
    if (name in symbolTable['GLOBAL'].keys()):
        for i,j in symbolTable['GLOBAL'][name].items():
                if (j['type'] == 'INT'):
                    return 'INT'
                elif (j['type'] == 'STRING'):
                    return 'STRING'
                elif (j['type'] == 'FLOAT'):
                    return 'FLOAT'
                else:
                    return None
    else:
        return None

def printSymbolTable():
    if err:
        pass
    else:
        for key in symbolTable:
            for keys in symbolTable[key]:
                print("Scope: %s, Name: %s, Value: %s" % (key, keys, symbolTable[key][keys]))


def printSymbolTablez():
    if err:
        pass
    else:
        for item in mainGlobal:
            print(item)
