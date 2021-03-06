from ply import lex
import fileinput
from irConverter import irConverter
from queue import *
import sys
import symboltable
from LinkedList import LinkedList
from ply import yacc
import traceback
from pprint import pprint

error = False

# List of token names.   This is always required
keywords = ('FUNCTION',
            'FLOAT',
            'PROGRAM',
            'STRING',
            'BEGIN',
            'ENDIF',
            'ENDWHILE',
            'END',
            'INT',
            'VOID',
            'READ',
            'WRITE',
            'IF',
            'ELSE',
            'WHILE',
            'CONTINUE',
            'BREAK',
            'RETURN')

tokens = keywords + (
    'KEYWORD',
    'IDENTIFIER',
    'OPERATOR',
    'STRINGLITERAL',
    'INTLITERAL',
    'FLOATLITERAL',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'COMMA',
    'SEMICOLON',
    'LPAREN',
    'RPAREN',
    'ASSIGN',
    'COMPOP'
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_MULTIPLY = r'\*'
t_ASSIGN = r':='
t_SEMICOLON = r';'
t_COMMA = r','

def t_COMPOP(t):
    r'<= | >= | < | > | != | ='
    return t

def t_KEYWORD(t):
    r'FUNCTION | FLOAT | PROGRAM | STRING | BEGIN | ENDIF | ENDWHILE | END | INT | VOID | READ | WRITE | IF | ELSE | WHILE | CONTINUE | BREAK | RETURN'
    if t.value in keywords:
        t.type = t.value
    return t

def t_STRINGLITERAL(t):
    r'(\'.*?\')|(\".*?\")'
    return t

t_FLOATLITERAL  = r'[0-9]+.[0-9]+'
t_INTLITERAL    = r'(?<![.])\b[0-9]+\b(?!\.[0-9])'
t_IDENTIFIER    = r'(?![0-9])([a-zA-Z0-9])+'

# A regular expression rule with some action code

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Define a rule so we can use comments
def t_COMMENT(t):
    r'--.*'
    pass
    #No return value so Token is discarded

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
#loop = fileinput.filename()
#with open (loop, "r") as myfile:
#    data = myfile.read()

data = ''
for line in fileinput.input(sys.argv[-1]):
    data += str(line)

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input

# Global Variables
ll = LinkedList()
registerNum = 1
labelNum = 1
stack = []
expression = []
q = Queue(maxsize=0)
typeExp = ""

# Program

print(";IR code")

def p_program(p):
    'program : PROGRAM id BEGIN pgm_body end'

def p_end(p):
    'end : END'
    print(";RET")
    ll.insert("RET", "", "", "")
    print(";tiny code")

def p_id(p):
    'id : IDENTIFIER'
    p[0] = p[1]

def p_program_body(p):
    'pgm_body : decl func_declarations '

def p_decl(p):
    '''decl : string_decl decl
    | var_decl decl
    | empty'''

# Global String Declaration

def p_string_decl(p):
    'string_decl : STRING id ASSIGN str SEMICOLON'
#    symbolTable[p[2]][p[4]] = (p[1],symbolTableInUse)
    symboltable.decl(p[2],p[1],p[4])

def p_str(p):
    'str : STRINGLITERAL'
    p[0] = p[1]

# Variable Declaration

def p_var_decl(p):
    'var_decl : var_type id_list SEMICOLON'
    for i in p[2]:
        symboltable.decl(i,p[1], 0)

def p_var_type(p):
    '''var_type : FLOAT
    | INT'''
    p[0] = p[1]


def p_any_type(p):
    '''any_type : var_type
    | VOID'''

def p_id_list(p):
    'id_list : id id_tail'
    p[0] = [p[1]] + p[2]

def p_id_tail(p):
    '''id_tail : COMMA id id_tail
    | empty'''
    if len(p) == 4:
        p[0]=[p[2]] + p[3]
    else:
        p[0]=[]

# Function Paramater List

def p_param_decl_list(p):
    '''param_decl_list : param_decl param_decl_tail
    | empty'''

def p_param_decl(p):
    'param_decl : var_type id'
    symboltable.decl(p[2],p[1],0)

def p_param_decl_tail(p):
    '''param_decl_tail : COMMA param_decl param_decl_tail
    | empty'''

# Function Declaration

def p_func_declarations(p):
    '''func_declarations : func_decl func_declarations
    | empty'''

def p_func_decl(p):
    '''func_decl : start_of_func LPAREN param_decl_list RPAREN BEGIN func_body END '''
    symboltable.mGlobal(0)

def p_start_of_func(p):
    '''start_of_func : FUNCTION any_type id'''
    symboltable.mGlobal(p[3])
    print(";LABEL " + p[3])
    ll.insert("LABEL", str(p[3]), "", "")
    print(";LINK")
    ll.insert("LINK", "", "", "")

def p_func_body(p):
    '''func_body : decl stmt_list '''

# Statement List

def p_stmt_list(p):
    '''stmt_list : stmt stmt_list
    | empty'''

def p_stmt(p):
    '''stmt : base_stmt
    | if_stmt
    | while_stmt '''

def p_base_stmt(p):
    '''base_stmt : assign_stmt
    | read_stmt
    | write_stmt
    | return_stmt '''

# Basic statements

def p_assign_stmt(p):
    '''assign_stmt : assign_expr SEMICOLON '''

def p_assign_expr(p):
    '''assign_expr : id ASSIGN expr '''
    global registerNum
    if (" " in p[3]):
        temp = str(p[1]) + " " + str(p[2]) + " " + str(p[3])
#        print(str(p[3]))
        irExpBuilder(temp)
    elif (symboltable.checkType(p[1]) == 'INT' and "." not in p[3]):
            print(";STOREI " + str(p[3]) + " $T" + str(registerNum))
            ll.insert("STOREI", str(p[3]), "$T" + str(registerNum), "")
            print(";STOREI $T" + str(registerNum) + " " + p[1])
            ll.insert("STOREI", "$T" + str(registerNum), p[1], "")
            registerNum = registerNum + 1
    elif (symboltable.checkType(p[1]) == 'FLOAT'):
        print(";STOREF " + str(p[3]) + " $T" + str(registerNum))
        ll.insert("STOREF", str(p[3]), "$T" + str(registerNum), "")
        print(";STOREF $T" + str(registerNum) + " " + p[1])
        ll.insert("STOREF", "$T" + str(registerNum), p[1], "")
        registerNum = registerNum + 1

def p_read_stmt(p):
    '''read_stmt : READ LPAREN id_list RPAREN SEMICOLON '''
    for i in p[3]:
        print(";READI " + str(i))
        ll.insert("READI", str(i), "", "")

def p_write_stmt(p):
    '''write_stmt : WRITE LPAREN id_list RPAREN SEMICOLON '''
    for i in p[3]:
        if (symboltable.checkType(i) == 'INT'):
            print(";WRITEI " + i)
            ll.insert("WRITEI", i, "", "")
        elif (symboltable.checkType(i) == 'STRING'):
            print(";WRITES " + i)
            ll.insert("WRITES", i, "", "")
        else:
            print(";WRITEF " + i)
            ll.insert("WRITEF", i, "", "")

def p_return_stmt(p):
    '''return_stmt : RETURN expr SEMICOLON '''

# Expressions

def p_expr(p):
    '''expr : expr_prefix factor '''
    global registerNum
    if (p[2] is None):
        p[0] = str(p[1])
    elif (p[1] is None):
        p[0] = str(p[2])
    else:
        p[0] = str(p[1]) + " " + str(p[2])

def p_expr_prefix(p):
    '''expr_prefix : expr_prefix factor addop
    | empty'''
    if len(p) > 2:
        if (p[1] != None):
            p[0] = str(p[1]) + " "  + str(p[2]) + " "  + str(p[3])
#            print("expr " + str(p[1]) + " ---- " + str(p[0]))
        else:
            p[0] = str(p[2]) + " "  + str(p[3])
#            print("expr " + str(p[1]) + " ----> " + str(p[0]))
#        expression.append(p[2])
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : factor_prefix postfix_expr '''
    if (p[2] is None):
        p[0] = str(p[1])
    elif (p[1] is None):
        p[0] = str(p[2])
    else:
        p[0] = str(p[1]) + " " + str(p[2])

def p_factor_prefix(p):
    '''factor_prefix : factor_prefix postfix_expr mulop
    | empty'''
    if (len(p) > 2):
        p[0] = str(p[2]) + " " + str(p[3])

def p_postfix_expr(p):
    '''postfix_expr : primary
    | call_expr '''
    p[0] = p[1]

def p_call_expr(p):
    '''call_expr : id LPAREN expr_list RPAREN '''

def p_expr_list(p):
    '''expr_list : expr expr_list_tail
    | empty'''

def p_expr_list_tail(p):
    '''expr_list_tail : COMMA expr expr_list_tail
    | empty'''
    if len(p) > 2:
        p[0] = [p[1], p[2], p[3]]

def p_primary(p):
    '''primary : LPAREN expr RPAREN
    | id
    | int_literal
    | float_literal'''
    if len(p) == 2:
        p[0] = p[1]
    else:
#        print(str(p[1]) + " " + str(p[2]) + " " + str(p[3]))
        p[0] = str(p[1]) + " " + str(p[2]) + " " +  str(p[3])
#        print(str(p[1]))

def p_int_literal(p):
    '''int_literal : INTLITERAL'''
    p[0] = p[1]

def p_float_literal(p):
    '''float_literal : FLOATLITERAL'''
    p[0] = p[1]

def p_addop(p):
    '''addop : PLUS
    | MINUS '''
    p[0] = p[1]

def p_mulop (p):
    '''mulop : MULTIPLY
    | DIVIDE '''
    p[0] = p[1]

# Complex Statements and conditions

def p_if_stmt(p):
    '''if_stmt : start_if LPAREN cond RPAREN decl stmt_list else_part end_if'''
    symboltable.block(0)

def p_start_if(p):
    '''start_if : IF'''
    symboltable.block(1)

def p_end_if(p):
    '''end_if : ENDIF'''
    global labelNum
    temp = stack.pop()
#    print("---"+str(labelNum))
    print(";LABEL label" + str(temp))
    ll.insert("LABEL", "label" + str(temp), "", "")

def p_else_part(p):
    '''else_part : start_else decl stmt_list
    | empty'''
    global labelNum
    if len(p) > 3:
        symboltable.block(0)
#        print(";LABEL label" + str(stack.pop()))
#        labelNum = labelNum + 1

def p_start_else(p):
    '''start_else : ELSE'''
    global labelNum
    symboltable.block(1)
#    print(labelNum)
    print(";JUMP label"+ str(labelNum))
    ll.insert("JUMP", "label" + str(labelNum), "", "")
    temp = stack.pop()
    print(";LABEL label" + str(temp))
    ll.insert("LABEL", "label" + str(temp), "", "")
    stack.append(labelNum)
#    print(";LABEL label" + str(queue))
    labelNum = labelNum + 1

def p_cond(p):
    '''cond : expr compop expr'''
    global labelNum
    global registerNum
    counter = 0;
    if (" " in p[3]):
        for i in p[3]:
            ops = ["*","/","-","+"]
            if (i in ops):
                counter = counter + 1

        counter = counter + registerNum + 2
        temp = "$T" + str(counter) + " := " + p[3]
        irExpBuilder(temp)
    else:
        if ("." not in p[3]):
            print(";STOREI " + str(p[3]) + " $T" + str(registerNum))
            ll.insert("STOREI", str(p[3]), "$T" + str(registerNum), "")
        else:
            print(";STOREF " + str(p[3]) + " $T" + str(registerNum))
            ll.insert("STOREF", str(p[3]), "$T" + str(registerNum), "")
#    print(labelNum)
    if (symboltable.checkType(p[1]) == 'INT'):
        typeExp = "I"
    elif (symboltable.checkType(p[1]) == 'FLOAT'):
        typeExp = "F"

    if (p[2] == '!='):
        print(";EQ" + typeExp + " " + str(p[1]) + " $T" + str(registerNum) + " label" + str(labelNum))
        ll.insert("EQ" + typeExp , str(p[1]), "$T" + str(registerNum), "label" + str(labelNum))
        q.put(labelNum)
        stack.append(labelNum)
        registerNum = registerNum + 1
        labelNum = labelNum + 1
    if (p[2] == '>'):
        print(";LE" + typeExp + " " + str(p[1]) + " $T" + str(registerNum) + " label" + str(labelNum))
        ll.insert("LE" + typeExp , str(p[1]), "$T" + str(registerNum), "label" + str(labelNum))
        q.put(labelNum)
        stack.append(labelNum)
        registerNum = registerNum + 1
        labelNum = labelNum + 1
    if (p[2] == '<'):
        print(";GE" + typeExp + " " + str(p[1]) + " $T" + str(registerNum) + " label" + str(labelNum))
        ll.insert("GE" + typeExp , str(p[1]), "$T" + str(registerNum), "label" + str(labelNum))
        q.put(labelNum)
        stack.append(labelNum)
        registerNum = registerNum + 1
        labelNum = labelNum + 1
    if (p[2] == '='):
        print(";NE" + typeExp + " " + str(p[1]) + " $T" + str(registerNum) + " label" + str(labelNum))
        ll.insert("NE" + typeExp , str(p[1]), "$T" + str(registerNum), "label" + str(labelNum))
        q.put(labelNum)
        stack.append(labelNum)
        registerNum = registerNum + 1
        labelNum = labelNum + 1
    if (p[2] == '<='):
        print(";GT" + typeExp + " " + str(p[1]) + " $T" + str(registerNum) + " label" + str(labelNum))
        ll.insert("GT" + typeExp , str(p[1]), "$T" + str(registerNum), "label" + str(labelNum))
        q.put(labelNum)
        stack.append(labelNum)
        registerNum = registerNum + 1
        labelNum = labelNum + 1
    if (p[2] == '>='):
        print(";LT" + typeExp + " " + str(p[1]) + " $T" + str(registerNum) + " label" + str(labelNum))
        ll.insert("LT" + typeExp , str(p[1]), "$T" + str(registerNum), "label" + str(labelNum))
        q.put(labelNum)
        stack.append(labelNum)
        registerNum = registerNum + 1
        labelNum = labelNum + 1

def p_compop(p):
    '''compop : COMPOP '''
    p[0] = p[1]

# While Statements

def p_while_stmt(p):
    '''while_stmt : start_while LPAREN cond RPAREN decl stmt_list end_while'''

def p_start_while(p):
    '''start_while : WHILE'''
    global labelNum
    symboltable.block(1)
    print(";LABEL label" + str(labelNum))
    ll.insert("LABEL", "label" + str(labelNum), "", "")
    q.put(labelNum)
    stack.append("label" + str(labelNum))
    labelNum = labelNum + 1

def p_end_while(p):
    '''end_while : ENDWHILE'''
    symboltable.block(0)
    temp = q.get()
    print(";JUMP label" + str(temp))
    ll.insert("JUMP", "label" + str(temp), "", "")
    global labelNum
    labelNum = labelNum + 1
    temp = q.get()
    print(";LABEL label" + str(temp))
    ll.insert("LABEL", "label" + str(temp), "", "")

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print("Not accepted")
    global error
    error = True

def irExpBuilder(expression):
    global registerNum
    global typeExp
    finalExpression = ""
    temp = expression.split(" ")
    counter = 0
    placeHolder = 0
    i = 0
    while i < len(temp):
        if ("." in temp[i]):
            print(";STOREF " + str(temp[i]) + " $T" + str(registerNum))
            ll.insert("STOREF", str(temp[i]) , "$T" + str(registerNum), "")
#                regDictionary['i'] = "$T" + registerNum
            temp[i] = "$T" + str(registerNum)
            typeExp = "F"
            registerNum = registerNum + 1
            i = 0
        elif (temp[i].isdigit()):
            print(";STOREI " + str(temp[i]) + " $T" + str(registerNum))
            ll.insert("STOREI", str(temp[i]) , "$T" + str(registerNum), "")
#                regDictionary['i'] = "$T" + registerNum
            temp[i] = "$T" + str(registerNum)
            typeExp = "I"
            registerNum = registerNum + 1
            i = 0
        else:
            i = i + 1

    i = 0
    while i < len(temp):
        if ('(' in temp[i]):
            placeHolder = i
            k = i
            j = 0
            while k < len(temp):
                if (')' in temp[k]):
                    j = k
                    break
                else:
                    k = k + 1
            temp.pop(placeHolder)
            j = j - 1
            temp.pop(j)
            j = j - 1
            i = innerExp(placeHolder, j, temp)
#                    print("MULTI " + temp[i-1])
        elif (len(temp) == 3):
            i = i + 1
        elif (i == len(temp)-1):
            placeHolder = 2
            i = innerExp(placeHolder, len(temp), temp)
        else:
            i = i + 1

    print(";STORE" + typeExp + " " + temp[2] + " " + temp[0])
    ll.insert("STORE" + typeExp, temp[2], temp[0], "")

def innerExp(start, end, listor):
    global registerNum
    global typeExp
    iterator = start
    ops = ['*','/','+','-']
    opNum = 0;
    for i in listor:
        if (symboltable.checkType(i) == 'INT'):
            typeExp = "I"
            break;
        elif (symboltable.checkType(i) == 'FLOAT'):
            typeExp = "F"
            break;

    while iterator < end:
        if (ops[0] in listor[iterator] or ops[1] in listor[iterator]):
            if (ops[0] in listor[iterator]):
                print(";MULT" + typeExp + " " + listor[iterator-1] + " " + listor[iterator + 1] + " $T" + str(registerNum))
                ll.insert("MULT" + typeExp, listor[iterator-1] , listor[iterator + 1], "$T" + str(registerNum))
                listor.insert(iterator-1, "$T" + str(registerNum))
                listor.pop(iterator)
                listor.pop(iterator)
                listor.pop(iterator)
                registerNum = registerNum + 1
                end = end - 2

            elif (ops[1] in listor[iterator] ):
                print(";DIV" + typeExp + " " + listor[iterator-1] + " " + listor[iterator + 1] + " $T" + str(registerNum))
                ll.insert("DIV" + typeExp, listor[iterator-1] , listor[iterator + 1], "$T" + str(registerNum))
                listor.insert(iterator-1, "$T" + str(registerNum))
                listor.pop(iterator)
                listor.pop(iterator)
                listor.pop(iterator)
                registerNum = registerNum + 1
                end = end - 2
                iterator = start + 1
        else:
            iterator = iterator + 1

    iterator = start
    while iterator < end:
        if (ops[2] in listor[iterator] or ops[3] in listor[iterator]):
            if (ops[2] in listor[iterator]):
                    print(";ADD" + typeExp + " " + listor[iterator-1] + " " + listor[iterator + 1] + " $T" + str(registerNum))
                    ll.insert("ADD" + typeExp, listor[iterator-1] , listor[iterator + 1], "$T" + str(registerNum))
                    listor.insert(iterator-1, "$T" + str(registerNum))
                    listor.pop(iterator)
                    listor.pop(iterator)
                    listor.pop(iterator)
                    registerNum = registerNum + 1
                    end = end - 2

            elif (ops[3] in listor[iterator]):
                    print(";SUB" + typeExp + " " + listor[iterator-1] + " " + listor[iterator + 1] + " $T" + str(registerNum))
                    ll.insert("SUB" + typeExp, listor[iterator-1] , listor[iterator + 1], "$T" + str(registerNum))
                    listor.insert(iterator-1, "$T" + str(registerNum))
                    listor.pop(iterator)
                    listor.pop(iterator)
                    listor.pop(iterator)
                    registerNum = registerNum + 1
                    end = end - 2
        else:
            iterator = iterator + 1

    if (len(listor) >= 2):
        registerNum = registerNum + 1
        return end
    else:
        listor.pop(end+1)
        return end

parser = yacc.yacc()

symboltable.mGlobal("GLOBAL")

parser.parse(data)



ir = irConverter(ll)

for i in symboltable.symbolTable['GLOBAL'].keys():
    for j,k in symboltable.symbolTable['GLOBAL'][i].items():
        if (k['type'] == 'INT'):
            print("var " + k['name'])

for i in symboltable.symbolTable['GLOBAL'].keys():
    for j,k in symboltable.symbolTable['GLOBAL'][i].items():
        if (k['type'] == 'FLOAT'):
            print("var " + k['name'])

for i in symboltable.symbolTable['GLOBAL'].keys():
    for j,k in symboltable.symbolTable['GLOBAL'][i].items():
        if (k['type'] == 'STRING'):
            print("str " + k['name'] + " " + k['value'])

ir.tinyBuilder()

#symboltable.mGlobal(0)

#if not error:
#    symboltable.printSymbolTable()
