# import os
import sys
import shlex

sys.argv.append('--!@#$%^&*()')

class EasmError(Exception):
    pass

if not '--!@#$%^&*()' in sys.argv:
    if '-d' in sys.argv or '--debug' in sys.argv:
        debug = True
        if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
            sys.argv.pop(1)
    else:
        debug = False

    if '-b' in sys.argv or '--binary' in sys.argv:
        print('Binary not implemented!')
        #binary = True
        binary = False
        if sys.argv[1] == '-b' or sys.argv[1] == '--binary':
            sys.argv.pop(1)
    else:
        binary = False

    try:
        if binary:
            with open(sys.argv[1], 'rb') as f:
                readlines = f.read().splitlines()
        else:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                readlines = f.read().splitlines()
        interactive = False
    except:
        interactive = True

else:
    debug = False
    binary = False
    interactive = False
    readlines = r'''show "Do you want to display the zen of python? "
; set the variable ans to: ask for value
strvar ans ask
; if ans == yes
; display the zen of python
if eq ans "yes" show "The Zen of Python, by Tim Peters\n\nBeautiful is better than ugly.\nExplicit is better than implicit.\nSimple is better than complex.\nComplex is better than complicated.\nFlat is better than nested.\nSparse is better than dense.\nReadability counts.\nSpecial cases aren't special enough to break the rules.\nAlthough practicality beats purity.\nErrors should never pass silently.\nUnless explicitly silenced.\nIn the face of ambiguity, refuse the temptation to guess.\nThere should be one-- and preferably only one --obvious way to do it.\nAlthough that way may not be obvious at first unless you're Dutch.\nNow is better than never.\nAlthough never is often better than *right* now.\nIf the implementation is hard to explain, it's a bad idea.\nIf the implementation is easy to explain, it may be a good idea.\nNamespaces are one honking great idea -- let's do more of those!"
; otherwise display other message
else show "You did not choose to show the zen of python."'''.splitlines()

exitprog = sys.exit


def pushint():
    statement = evaleasm()
    #print(statement,type(statement))
    if statement is not None and type(statement) == int:
        int_stack.append(statement)
    else:
        raiseerror('Error in pushint!')
    return None


def pushstr():
    statement = evaleasm()
    if statement and type(statement) == str:
        str_stack.append(statement)
    else:
        raiseerror('Error in pushstr!')
    return None


def pullint():
    return int_stack.pop()


def pullstr():
    return str_stack.pop()


def peekint():
    return int_stack[-1]


def peekstr():
    return str_stack[-1]


def string():
    return str(evaleasm())


def toint():
    return int(evaleasm())


def add():
    return int_stack[-1] + int_stack[-2]


def mult():
    return int_stack[-1] * int_stack[-2]


def div():
    return str(int_stack[-1] / int_stack[-2])


def concat():
    return str_stack[-2] + str_stack[-1]


def strvar():
    var_name = evaleasm(isname=True)
    statement = evaleasm()
    if statement and type(statement) == str:
        str_vars.update({var_name: statement})
    else:
        raiseerror('Error in strvar!')

    return None


def intvar():
    var_name = evaleasm(isname=True)
    statement = evaleasm()
    if statement and type(statement) == int:
        int_vars.update({var_name: statement})
    else:
        raiseerror('Error in intvar!')

    return None

def eif():
    global is_if
    if bool(evaleasm()):
        is_if=True
        evaleasm()
    else:
        is_if = False

def eelse():
    global is_if
    if not is_if:
        evaleasm()
        is_if = True

def eq():
    one = evaleasm()
    two = evaleasm()
    if one == two:
        return 1
    else:
        return 0

def ask():
    return input()


def show():
    statement = evaleasm()
    # print([statement], [type(statement)])
    if statement and type(statement) == str:
        if interactive:
            print(statement)
        else:
            print(statement, end='')
    else:
        raiseerror('Error in show!')
    # print('n')

    return None


proglines = []
coms = {'pushint': pushint, 'pushstr': pushstr, 'pullint': pullint, 'pullstr': pullstr, 'peekint': peekint,
        'peekstr': peekstr, 'string': string, 'int': toint, 'concat': concat,
        'show': show, 'add': add, 'mult': mult, 'div': div, 'exit': exitprog,
        'intvar': intvar, 'strvar': strvar,'ask':ask,'if':eif,'else':eelse,'eq':eq}

# coms = ['pushint', 'pushstr', 'pullint', 'pullstr', 'string', 'int', 'show']
is_if=True

str_stack = []
int_stack = []
str_vars  = {}
int_vars  = {}


def tonum(num):
    try:
        return int(num)
    except:
        return False


# tonum = int

def tostr(txt):
    if txt.startswith('"') and txt.endswith('"'):
        return txt.removeprefix('"').removesuffix('"').replace(r'\n', '\n')
    else:
        return False


# tostr = str

def iscom(com):
    if com in coms:
        return True
    else:
        return False


def isintvar(statement):
    if statement in int_vars.keys():
        return True
    else:
        return False


def isstrvar(statement):
    if statement in str_vars.keys():
        return True
    else:
        return False


# print('\n'.join(proglines))

def raiseerror(err):
    sys.stderr.write('Error: ' + err)
    sys.exit()


def evaleasm(isname=False):
    statement = prog[r].pop(0)
    if isname:
        return statement
    isstr = tostr(statement)
    isnum = tonum(statement)
    is_com = iscom(statement)
    is_strvar = isstrvar(statement)
    is_intvar = isintvar(statement)

    if debug:
        # print('statement:',statement,'| is string:', [isstr],'| is num:', [isnum],'| int stack:', int_stack,'| str stack:', str_stack)
        print('statement:', [statement], 'is command:', [is_com], 'is string:', [isstr], 'is num:', [isnum],
              'is str var:', [is_strvar], 'is int var:', [is_intvar], 'int stack:', int_stack,
              'str stack:', str_stack, 'str vars:', [str_vars], 'int vars:', [int_vars],'is if',is_if)
    #print(isnum is not None)
    if isnum is not False:
        return isnum
    if isstr is not False:
        # print(isstr)
        return isstr
    if is_com is not False:
        return coms[statement]()
    if is_strvar is not False:
        # print(str_vars, statement)
        return str_vars[statement]
    if is_intvar is not False:
        return int_vars[statement]


prog = []
r = 0
if not interactive:
    for x in readlines:
        if x:
            if not x.startswith(';'):
                proglines.append(x)

    for x, line in enumerate(proglines):
        prog.append([])
        for com in shlex.split(line, posix=False):
            prog[x].append(com)

    if prog:
        for x, item in enumerate(prog):
            r = x
            evaleasm()
else:
    if debug:
        print('Easm Interactive - Debug Mode:')
    else:
        print('Easm Interactive:')
    while True:
        prog = [[]]
        line = input('> ')
        for com in shlex.split(line, posix=False):
            prog[0].append(com)
        if prog[0]:
            for x, item in enumerate(prog):
                r = x
                evaleasm()

# print(prog)
