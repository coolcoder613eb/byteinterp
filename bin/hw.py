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
    readlines = '''show "Hello World!"'''.splitlines()

exitprog = sys.exit


def pushint():
    statement = evaleasm()
    if statement and type(statement) == int:
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
    return int(str_stack.pop())


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
        'intvar': intvar, 'strvar': strvar}
bincoms = {b'\x00': pushint, b'\x01': pushstr, b'\x02': pullint, b'\x03': pullstr, b'\x04': peekint, b'\x05': peekstr,
           b'\x06': string, b'\x07': toint, b'\x08': concat, b'\x09': show, b'\x0a': add, b'\x0b': mult, b'\x0c': div,
           b'\x0d': exitprog, b'\x0e': intvar, b'\x0f': strvar}

# coms = ['pushint', 'pushstr', 'pullint', 'pullstr', 'string', 'int', 'show']

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
    if not binary:
        if com in coms:
            return True
        else:
            return False
    else:
        if com in bincoms:
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
              'str stack:', str_stack, 'str vars:', [str_vars], 'int vars:', [int_vars])
    if is_com:
        if not binary:
            return coms[statement]()
        else:
            return bincoms[statement]()
    if is_strvar:
        # print(str_vars, statement)
        return str_vars[statement]
    if is_intvar:
        return int_vars[statement]
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
