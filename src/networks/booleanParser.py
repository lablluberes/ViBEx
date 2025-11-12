
###########################################################
# Parsing Boolean Functions
# # This version takes string Boolean function: "A or B" and applies dictionary variables values: {'A': True, 'B': False}
# Based on: https://github.com/dabeaz/ply/blob/master/example/calc/calc.py
###########################################################

# tokens for parser
tokens = (
    'AND','OR','NOT','XOR',
    'LPAREN','RPAREN', 'NAME', 'TRUE', 'FALSE'
    )

# Tokens

t_AND    = r'and'
t_OR   = r'or'
t_NOT  = r'not'
t_XOR = r'\^'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_TRUE = 'True'
t_FALSE = 'False'

# Ignored characters
t_ignore = " \t"

#taken from https://stackoverflow.com/questions/69140009/ply-expression-in-grammar-causes-symbol-error
# this is to verify reverded tokens "and", "or", "not"
reserved = {
  'and':'AND',
  'or':'OR',
  'not':'NOT',
  'True':'TRUE',
  'False':'FALSE'
}

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value,'NAME')    # Check for reserved words
  return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

#precedence = (
#    ('left','PLUS','MINUS'),
#    ('left','TIMES','DIVIDE'),
#    ('right','UMINUS'),
#    )


# dictionary of names
names = { }

#def p_statement_assign(t):
#   'statement : NAME EQUALS expression'
#    names[t[1]] = bool(t[3])
#    print(names)

#def p_statement_expr(t):
#    'expression : expression'
#    print("calculated:", t[1])

# parses NOT boolean expression
def p_expression_not(t):
    '''
    expression : NOT expression
    '''
    #print(t)
    if t[1] == 'not':
        t[0] = not t[2]

# parses AND, OR, XOR boolean expressions
def p_expression_binop(t):
    '''expression : expression AND expression
                  | expression OR expression
                  | expression XOR expression'''
    if t[2] == 'and': 
        t[0] = t[1] and t[3]
    elif t[2] == 'or':
        t[0] = t[1] or t[3]
    elif t[2] == '^':
        t[0] = t[1] ^ t[3]

# parses expression inside parenthesis
def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

# once a variable name search for boolean value inside dictionary
def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

# parses TRUE or FALSE expression and returns boolean value   
def p_expression_bool(t):
    '''expression : TRUE
                | FALSE'''
    
    if t[1] == 'True':
        t[0] = True
    elif t[1] == 'False':
        t[0] = False

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

# example 

def runBooleanParser(values, expr):

    #values = {'a':True, 'b':False}
    global names
    names = values

    return parser.parse(expr)

