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
    if (p[3][0] is None):
        if ((symboltable.checkType(p[3][1]) != 'FLOAT' and symboltable.checkType(p[3][1]) != 'STRING') and "." not in p[3][1]):
            print(";STOREI " + str(p[3][1]) + " $T" + str(registerNum))
            ll.insert("STOREI", str(p[3][1]), "$T" + str(registerNum), "")
            print(";STOREI $T" + str(registerNum) + " " + p[1])
            ll.insert("STOREI", "$T" + str(registerNum), p[1], "")
            registerNum = registerNum + 1
        elif (symboltable.checkType(p[3][1]) == 'FLOAT' and symboltable.checkType(p[1]) == 'FLOAT'):
            print(";STOREF " + str(p[3][1]) + " " + p[1])
        elif (symboltable.checkType(p[3][1]) == 'FLOAT' or "." in p[3][1]):
            print(";STOREF " + str(p[3][1]) + " $T" + str(registerNum))
            ll.insert("STOREF", str(p[3][1]), "$T" + str(registerNum), "")
            print(";STOREF $T" + str(registerNum) + " " + p[1])
            ll.insert("STOREF", "$T" + str(registerNum), p[1], "")
            registerNum = registerNum + 1
    if (p[3][0] is not None):
        if ("$T" in p[3][0]):
            print(";STOREI $T" + str(p[3][2]) + " " + str(p[1]))
        elif (symboltable.checkType(p[3][1]) == 'INT' or "." not in p[3][1]):
            print(";STOREI $T" + str(p[3][2]) + " " + str(p[3][0]))
            ll.insert("STOREI", "$T" + str(p[3][2]), str(p[3][0]), "")
        else:
            print(";STOREF $T" + str(p[3][2]) + " " + str(p[3][0]))
            ll.insert("STOREF", "$T" + str(p[3][2]), str(p[3][0]), "")

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
    print(str(p[0]) + " " + str(p[1]))
    if (p[1] is not None):
        temp = registerNum
        if ("$T" not in p[2] and symboltable.checkType(p[2]) is None):
            print(";STOREI " + str(p[2]) + " $T" + str(registerNum))
            ll.insert("STOREI", str(p[2]), "$T" + str(registerNum), "")
            temp = registerNum + 1
            if (p[1][1] == '+'):
                print(";ADDI " + p[1][0] + " $T" + str(registerNum) + " $T" + str(temp))
                ll.insert("ADDI", str(p[1][0]), "$T" + str(registerNum), "$T" + str(temp))
                registerNum = registerNum + 2
            elif(p[1][1] == '-'):
                print(";SUBI " + p[1][0] + " $T" + str(registerNum) + " $T" + str(temp))
                ll.insert("SUBI", str(p[1][0]), "$T" + str(registerNum), "$T" + str(temp))
                registerNum = registerNum + 2
        elif ("$T" in p[1][0] or "$T" in p[2]):
            if (p[1][1] == '+'):
                print(";ADDI " + p[1][0] + " " + str(p[2]) + " $T" + str(temp))
                ll.insert("ADDI", str(p[1][0]), str(p[2]), "$T" + str(temp))
                registerNum = registerNum + 1
            elif(p[1][1] == '-'):
                print(";SUBI " + p[1][0] + " " + str(p[2]) + " $T" + str(temp))
                ll.insert("SUBI", str(p[1][0]), str(p[2]), "$T" + str(temp))
                registerNum = registerNum + 2
        elif ("$T" not in p[1][0] or "$T" not in p[2]):
            if (p[1][1] == '+'):
                print(";ADDI " + p[1][0] + " " + str(p[2]) + " $T" + str(temp))
                ll.insert("ADDI", str(p[1][0]), str(p[2]), "$T" + str(temp))
                registerNum = registerNum + 1
            elif(p[1][1] == '-'):
                print(";SUBI " + p[1][0] + " " + str(p[2]) + " $T" + str(temp))
                ll.insert("SUBI", str(p[1][0]), str(p[2]), "$T" + str(temp))
                registerNum = registerNum + 2
        p[0] = [p[1][0],p[2],temp]
    else:
        p[0] = [p[1],p[2]]

def p_expr_prefix(p):
    '''expr_prefix : expr_prefix factor addop
    | empty'''
    if len(p) == 4:
        p[0] = [p[2],p[3]]
        expression.append(p[2])
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : factor_prefix postfix_expr '''
    p[0] = p[2]
    global registerNum
    if (p[1] is not None and p[1][1] == '*'):
        print(";MULTI " + p[1][0] + " " + p[2] + " $T" + str(registerNum))
        ll.insert("MULTI", str(p[1][0]), str(p[2]),  str("$T" + str(registerNum)))
        tempReg = "$T"+str(registerNum)
        registerNum = registerNum + 1
        p[0] = tempReg

def p_factor_prefix(p):
    '''factor_prefix : factor_prefix postfix_expr mulop
    | empty'''
    if (len(p) > 2):
        p[0] = [p[2],p[3]]
        print(p[0])

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

def p_primary(p):
    '''primary : LPAREN expr RPAREN
    | id
    | int_literal
    | float_literal'''
    if len(p) == 2:
        p[0] = p[1]
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
    print(";STOREI " + str(p[3][1]) + " $T" + str(registerNum))
    ll.insert("STOREI", str(p[3][1]), "$T" + str(registerNum), "")
#    print(labelNum)
    if (p[2] == '!='):
        print(";EQI " + str(p[1][1]) + " $T" + str(registerNum) + " label" + str(labelNum))
        ll.insert("EQI", str(p[1][1]), "$T" + str(registerNum), "label" + str(labelNum))
        q.put(labelNum)
        stack.append(labelNum)
        registerNum = registerNum + 1
        labelNum = labelNum + 1
    if (p[2] == '>'):
        print(";LEI " + str(p[1][1]) + " $T" + str(registerNum) + " label" + str(labelNum))
        ll.insert("LEI", str(p[1][1]), "$T" + str(registerNum), "label" + str(labelNum))
        q.put(labelNum)
        stack.append(labelNum)
        registerNum = registerNum + 1
        labelNum = labelNum + 1
    if (p[2] == '<'):
        print(";GEI " + str(p[1][1]) + " $T" + str(registerNum) + " label" + str(labelNum))
        ll.insert("GEI", str(p[1][1]), "$T" + str(registerNum), "label" + str(labelNum))
        q.put(labelNum)
        stack.append(labelNum)
        registerNum = registerNum + 1
        labelNum = labelNum + 1

def p_compop(p):
    '''compop : COMPOP '''
    global labelNum
    p[0] = p[1]
    if (p[1] == '='):
        print(";NEI")
    if (p[1] == '<='):
        print(";GTI")
    if (p[1] == '<'):
        p[0] = p[1]
    if (p[1] == '>='):
        print(";LTI")
    if (p[1] == '>'):
#        print(";LEI label" + str(labelNum))
        p[0] = p[1]
    else:
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
        if (k['type'] == 'STRING'):
            print("str " + k['name'] + " " + k['value'])

ir.tinyBuilder()

#symboltable.mGlobal(0)

#if not error:
#    symboltable.printSymbolTable()
