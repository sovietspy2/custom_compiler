import ply.lex as lex
import ply.yacc as yacc
import sys
from pathlib import Path
import re

# Create a list to hold all of the token names
tokens = [

    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS',
    'DRAW',
    'FOR',
    'OPEN',
    'CLOSE',
    'OPEN_P',
    'CLOSE_P',
    'SEMICOLON',
    'STRING',
    'Q_MARK',
    'PRINT',
    'IF',
    'EQUALEQUAL',
    'LESS',
    'MORE',
    'ELSE',
    'INPUT'

]

# Use regular expressions to define what each token is
t_EQUALEQUAL = "=="
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\='
#t_DRAW = "DRAW"
#t_FOR = "FOR"
t_OPEN = r'\{'
t_CLOSE = r'\}'
t_OPEN_P = r'\('
t_CLOSE_P = r'\)'
t_SEMICOLON = r'\;'
t_Q_MARK = r"\""

t_LESS = r'\<'
t_MORE = r'\>'
t_INPUT = r'INPUT'
#t_PRINT = "PRINT"

# Ply's special t_ignore variable allows us to define characters the lexer will ignore.
# We're ignoring spaces.
t_ignore = ' \n'

# More complicated tokens, such as tokens that are more than 1 character in length
# are defined using functions.
# A float is 1 or more numbers followed by a dot (.) followed by 1 or more numbers again.

# def t_INPUT(t):
#     "INPUT"
#     t.type = "INPUT"
#     return t

def t_ELSE(t):
    "ELSE"
    t.type = "ELSE"
    return t

def t_IF(t):
    "IF"
    t.type = "IF"
    return t

def t_STRING(t):
    r'\"[a-zA-Z_][a-zA-Z_0-9]*\"'
    t.type = "STRING"
    t.value = str(t.value)
    return t

def t_DRAW(t):
    "DRAW"
    t.type = "DRAW"
    return t

def t_FOR(t):
    "FOR"
    t.type = "FOR"
    return t

def t_PRINT(t):
    "PRINT"
    t.type = "PRINT"
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# An int is 1 or more numbers.
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# A NAME is a variable name. A variable can be 1 or more characters in length.
# The first character must be in the ranges a-z A-Z or be an underscore.
# Any character following the first character can be a-z A-Z 0-9 or an underscore.
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t

# Skip the current token and output 'Illegal characters' using the special Ply t_error function.
def t_error(t):
    print("Illegal characters!")
    t.lexer.skip(1)

def t_COMMENT(t):
    r'\//.*'
    pass
    # No return value. Token discarded

# Build the lexer
lexer = lex.lex()

# Ensure our parser understands the correct order of operations.
# The precedence variable is a special Ply variable.
precedence = (

    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),

)

# Define our grammar. We allow expressions, var_assign's and empty's.


def p_start(p): # Itt kezdődik
    '''
    run : expression
         | var_assign
         | condition
         | empty

    '''
    print(p[1])
    run(p[1])



def p_var_assign2(p): #
    '''
    var_assign : NAME EQUALS expression SEMICOLON var_assign
               | NAME EQUALS expression SEMICOLON expression
               | NAME EQUALS expression expression
    '''
    # Build our tree
    p[0] = ('=', p[1], p[3], p[5])

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression SEMICOLON
    var_assign : NAME EQUALS INPUT SEMICOLON
    '''
    # Build our tree
    p[0] = ('=', p[1], p[3], None)

# Expressions are recursive.

def p_expression(p): # + - / * operators
    '''
    expression : expression MULTIPLY expression SEMICOLON
               | expression DIVIDE expression SEMICOLON
               | expression PLUS expression SEMICOLON
               | expression MINUS expression SEMICOLON
    '''
    # Build our tree.
    #print((p[2], p[1], p[3]))
    p[0] = (p[2], p[1], p[3])


def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
               | STRING
    '''
    p[0] = p[1]

def p_expression_var(p):
    '''
    expression : NAME
    '''
    p[0] = ('VAR', p[1])

def p_draw(p): # X1 Y1 X2 Y2
    '''
    expression : DRAW OPEN_P expression expression expression expression CLOSE_P SEMICOLON
    '''
    p[0] = ('DRAW', p[3], p[4], p[5], p[6])

def p_for2(p):
    '''
    expression : FOR OPEN_P INT CLOSE_P OPEN var_assign CLOSE expression
               | FOR OPEN_P INT CLOSE_P OPEN expression CLOSE expression
               | FOR OPEN_P INT CLOSE_P OPEN expression CLOSE var_assign
               | FOR OPEN_P INT CLOSE_P OPEN var_assign CLOSE var_assign
    '''
    p[0] = ('FOR', p[3], p[6], p[8])

def p_for(p):
    '''
    expression : FOR OPEN_P INT CLOSE_P OPEN var_assign CLOSE
               | FOR OPEN_P INT CLOSE_P OPEN expression CLOSE
    '''
    p[0] = ('FOR', p[3], p[6], None)


def p_print2(p):
    '''
    expression : PRINT expression SEMICOLON expression
               | PRINT expression SEMICOLON var_assign
    '''
    p[0] = ('PRINT', p[2], p[4])

def p_print(p):
    '''
    expression : PRINT expression SEMICOLON
    '''
    p[0] = ('PRINT',p[2], None)

def p_condition(p):
    '''
    condition : INT LESS INT
              | INT MORE INT
              | INT EQUALEQUAL INT
    '''
    p[0] = (p[2], p[1], p[3])

def p_if_way(p):
    '''
    expression : IF OPEN_P condition CLOSE_P OPEN expression CLOSE
               | IF OPEN_P condition CLOSE_P OPEN var_assign CLOSE
    '''
    p[0] = (p[1], p[3], p[6], None)

def p_if_way2(p):
    '''
    expression : IF OPEN_P condition CLOSE_P OPEN expression CLOSE expression
               | IF OPEN_P condition CLOSE_P OPEN var_assign CLOSE expression
               | IF OPEN_P condition CLOSE_P OPEN var_assign CLOSE var_assign
               | IF OPEN_P condition CLOSE_P OPEN expression CLOSE var_assign
    '''
    p[0] = (p[1], p[3], p[6], p[8], None, None)

def p_if_way_else(p):
    '''
    expression : IF OPEN_P condition CLOSE_P OPEN expression CLOSE ELSE OPEN expression CLOSE
               | IF OPEN_P condition CLOSE_P OPEN var_assign CLOSE ELSE OPEN expression CLOSE
               | IF OPEN_P condition CLOSE_P OPEN var_assign CLOSE ELSE OPEN var_assign CLOSE
               | IF OPEN_P condition CLOSE_P OPEN expression CLOSE ELSE OPEN var_assign CLOSE
    '''
    p[0] = (p[1], p[3], p[6], p[8], p[10], None)

def p_if_way_else_plus_expression(p):
    '''
    expression : IF OPEN_P condition CLOSE_P OPEN expression CLOSE ELSE OPEN expression CLOSE expression
               | IF OPEN_P condition CLOSE_P OPEN var_assign CLOSE ELSE OPEN expression CLOSE expression
               | IF OPEN_P condition CLOSE_P OPEN var_assign CLOSE ELSE OPEN var_assign CLOSE expression
               | IF OPEN_P condition CLOSE_P OPEN var_assign CLOSE ELSE OPEN var_assign CLOSE var_assign
               | IF OPEN_P condition CLOSE_P OPEN expression CLOSE ELSE OPEN var_assign CLOSE expression
               | IF OPEN_P condition CLOSE_P OPEN expression CLOSE ELSE OPEN expression CLOSE var_assign
    '''
    p[0] = (p[1], p[3], p[6], p[8], p[10], p[12])

# def p_else(p):
#     '''
#     expression :
#     '''


# Output to the user that there is an error in the input as it doesn't conform to our grammar.
# p_error is another special Ply function.
def p_error(p):
    print("Syntax error found! {}".format(p))

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# Build the parser
parser = yacc.yacc()
# Create the environment upon which we will store and retreive variables from.
env = {}
identifier = 0
switch = False
tab_holder = ""
helper_string = ""
inline = False
one_less_tab_in_cycle = False
# The run function is our recursive function that 'walks' the tree generated by our parser.
def run(p):
    global identifier
    identifier = identifier+1
    global env
    global switch
    line = ""
    global tab_holder
    global helper_string
    global inline
    global one_less_tab_in_cycle
    if type(p) == tuple:
        if p[0] in ('+','-','*','/','!'):

            if switch is True:
                line = tab_holder

            if type(p[1]) is tuple:
                helper_string = line + "{}{}".format(p[0], p[2]) + helper_string
                return run(p[1])
            else:
                helper_string = line + "{}{}{}".format(p[1],p[0] ,p[2]) + helper_string
                if inline is False:
                    compiled_lines.append(helper_string)
                else:

                    if one_less_tab_in_cycle is True:  # Néha plusz tab bekerült ehhez új változó kellett
                        return_value = re.sub('\t', '' ,helper_string)

                    helper_string = ""
                    return return_value

                return_value = helper_string
                helper_string = ''
                return return_value

            #return run(p[1]) + run(p[2])
        elif p[0] == '=':
            if switch is True:
                line = tab_holder
            inline = True
            one_less_tab_in_cycle = True
            env[p[1]] = run(p[2])
            inline = False
            one_less_tab_in_cycle = False
            line += "{} = {}".format(p[1], env[p[1]])

            compiled_lines.append(line)
            #line = ""
            run(p[3]) #_type_of_literal(),
            return ''
        elif p[0] == 'VAR':
            if p[1] == 'INPUT':
                return 'input(\'>>\')'
            if p[1] not in env:
                # if p[1] == 'i' and switch is True:
                #     return env[p[1]]
                # else:
                    raise NameError('Undeclared variable found!')
            else:
                return env[p[1]]
        elif p[0] == 'DRAW':
            line += "w.create_line({}, {}, {}, {})".format(p[1],p[2],p[3],p[4])
            compiled_lines.append(line)

        elif p[0] == 'FOR': ##############################################FOR
            if switch is True:
                line = tab_holder
            line += "for i in range(0,{}): \n".format(p[1])
            if 'i' not in env.values():
                env['i'] = ' '
            compiled_lines.append(line)
            switch = True
            tab_holder += "\t"

            run(p[2])


            tab_holder = tab_holder[:-1]
            run(p[3])
            switch = False

        elif p[0] == 'PRINT':

            if type(p[1]) is tuple:
                inline = True
                var = run(p[1])
                inline = False
            else:
                var = p[1]
            if switch is True:
                line = tab_holder
            try:
                if p[1][0] == "VAR": # ha van benne komplex
                    var = p[1][1]
            except TypeError: # my job is done here
                pass
            # if var[:1] == "\"": # Ha sztring akkor lehagyom az idézőjeleket
            #     var = var[1:-1]
            line += 'print({})'.format(var)
            compiled_lines.append(line)
            #line = ''
            run(p[2])
        elif p[0] in ('<', '==', '>'):

            if switch is True:
                line = tab_holder

            if inline is True:
                return '{} {} {}'.format(p[1],p[0],p[2])
            else:
                compiled_lines.append('{} {} {}'.format(p[1],p[0],p[2]))
        elif p[0] in ('IF'):

            if switch is True:
                line = tab_holder

            inline = True
            line += 'if ({}):'.format(run(p[1]))
            compiled_lines.append(line)
            inline = False

            switch = True
            tab_holder += '\t'
            run(p[2])
            tab_holder = tab_holder[:-1]

            if p[3] == 'ELSE':
                line = ''
                if switch is True:
                    line = tab_holder

                line += 'else:'
                compiled_lines.append(line)
                switch = True
                tab_holder += '\t'
                run(p[4])
                tab_holder = tab_holder[:-1]
                switch = False
            else:
                run(p[3])
            switch = False
    else:
        return p

# Create a REPL to provide a way to interface with our calculator.
# while True:
#     try:
#         s = input('')
#     except EOFError:
#         break
#     parser.parse(s)


p = Path('program.x')
lines = p.read_text()
compiled_lines = []

#for line in lines:
parser.parse(lines)

with open('program.py', 'a') as the_file:
    if not compiled_lines:
        print("Error occured! no lines to write")
    else:
        first_lines ="""
from tkinter import *
master = Tk()
master.winfo_toplevel().title("X language demo")
w = Canvas(master, width=1280, height=720)
w.pack()

w.create_line(0, 0, 1280, 720)
"""

        #compiled_lines.insert(0, first_lines)

        #compiled_lines.append("master.mainloop()")

        for line in compiled_lines:
            the_file.write(line+'\n')

