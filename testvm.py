from vm import *
import sys, os
HALT  = 0
PUSH  = 1
ADD   = 2
SUB   = 3
MUL   = 4
DIV   = 5
NOT   = 6
AND   = 7
OR    = 8
POP   = 9
DUP   = 10
ISEQ  = 11
ISGT  = 12
JMP   = 13
JIF   = 14
LOAD  = 15
STORE = 16

decode = dict(HALT  = 0,
PUSH  = 1,
ADD   = 2,
SUB   = 3,
MUL   = 4,
DIV   = 5,
NOT   = 6,
AND   = 7,
OR    = 8,
POP   = 9,
DUP   = 10,
ISEQ  = 11,
ISGT  = 12,
JMP   = 13,
JIF   = 14,
LOAD  = 15,
STORE = 16)
print(decode)
with open(sys.argv[1] if len(sys.argv) > 1 else os.devnull,'r',encoding='utf-8') as f:
    print(f.read())

test([i.PUSH,42,i.PUSH,43,i.HALT],False)
test([i.PUSH,1,i.PUSH,2,i.ADD,i.HALT],False)
test([i.PUSH,5,i.PUSH,3,i.DIV,i.HALT],False)
#test([i.SUB,i.HALT],False)
test([i.PUSH,1,i.NOT,i.PUSH,0,i.NOT,i.HALT],False)
test([i.PUSH,1,i.PUSH,0,i.AND,i.HALT],False)
test([i.PUSH,1,i.PUSH,32,i.DUP,i.HALT],False)
test([i.JMP,5,i.PUSH,32,i.DUP,i.PUSH,5,i.HALT],False)
test([i.PUSH, 1, i.JIF, 5, i.POP, i.PUSH, 0, i.JIF, 4, i.HALT],False)
test([i.PUSH, 1,i.PUSH, 32, i.STORE, 5, i.POP, i.PUSH, 0, i.LOAD, 5, i.HALT],False)

test([PUSH, 6,
    STORE, 0,

    # Init b with "4"
    PUSH, 4,
    STORE, 1,

    # Load a and b into the stack
    LOAD, 0,            # Stack contains a
    LOAD, 1,            # Stack contains a, b
    ISGT,               # Stack contains a > b
    JIF, 21,

    # This is the "else" path
    LOAD, 1,            # Stack contains b
    STORE, 2,           # Set c to the stack head, meaning c = b
    JMP, 25,

    # This is the "if" path, and this is the address 21
    LOAD, 0,            # Stack contains a
    STORE, 2,           # Set c to the stack head, meaning c = a

    # Done; this is address 25
    HALT],False)
test([
    # Init a with "6"
    PUSH, 6,
    STORE, 0,

    # Init b with "4"
    PUSH, 4,
    STORE, 1,

    # Init total to 0
    PUSH, 0,
    STORE, 2,

    # While part
    # Here is address 12
    LOAD, 1,            # Stack contains b
    PUSH, 0,            # Stack contains b, 1
    ISGT,               # Stack contains b >= 1
    NOT,                # Stack contains b < 1
    JIF, 36,            # 36 is the address of the HALT label

    # Inner loop part
    LOAD, 0,            # Stack contains a
    LOAD, 2,            # Stack contains a, total
    ADD,                # Stack contains a + total
    STORE, 2,           # Save in total, meaning total = a + total

    LOAD, 1,            # Stack contains b
    PUSH, 1,            # Stack contains b, 1
    SUB,                # Stack contains b - 1
    STORE, 1,           # Save in b, meaning b = b - 1

    JMP, 12,            # Go back to the start of the loop

    HALT],True
)
