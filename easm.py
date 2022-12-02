import os
import sys
import shlex

class EasmError(Exception):
    pass

try:
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        readlines = f.read().splitlines()
    interactive = False
except:
    interactive = True

if '-d' in sys.argv or '--debug' in sys.argv:
    debug = True
else:
    debug = False

exitprog = sys.exit


def pushint():
    statement = evaleasm()
    if statement and type(statement) == int:
        int_stack.append(statement)
    else:
        raise EasmError('Error!')
    return None


def pushstr():
    statement = evaleasm()
    if statement and type(statement) == str:
        str_stack.append(statement)
    else:
        raise EasmError('Error!')
    return None


def pullint():
    return int_stack.pop()


def pullstr():
    return str_stack.pop()


def string():
    return str(int_stack.pop())


def toint():
    return int(str_stack.pop())


def add():
    return int_stack[-1] + int_stack[-2]


def mult():
    return int_stack[-1] * int_stack[-2]


def div():
    return str(int_stack[-1] / int_stack[-2])


def show():
    statement = evaleasm()
    if statement and type(statement) == str:
        if interactive:
            print(statement)
        else:
            print(statement, end='')
    else:
        raise EasmError('Error!')
    # print('n')

    return None


proglines = []
coms = {'pushint': pushint, 'pushstr': pushstr, 'pullint': pullint, 'pullstr': pullstr, 'string': string, 'int': toint,
        'show': show, 'add': add, 'mult':mult , 'div': div, 'exit': exitprog}

# coms = ['pushint', 'pushstr', 'pullint', 'pullstr', 'string', 'int', 'show']

str_stack = []
int_stack = []


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


# print('\n'.join(proglines))


def evaleasm():
    statement = prog[r].pop(0)
    isstr = tostr(statement)
    isnum = tonum(statement)
    if debug:
        # print('statement:',statement,'| is string:', [isstr],'| is num:', [isnum],'| int stack:', int_stack,'| str stack:', str_stack)
        print('statement:', [statement], 'is string:', [isstr], 'is num:', [isnum], 'int stack:', int_stack,
              'str stack:', str_stack)
    if iscom(statement):
        return coms[statement]()
    if isnum:
        return isnum
    if isstr:
        # print(isstr)
        return isstr


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
