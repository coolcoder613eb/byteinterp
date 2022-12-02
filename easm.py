import sys
import shlex

with open(sys.argv[1],'r',encoding='utf-8') as f:
    readlines = f.read().splitlines()

proglines = []

str_stack = []
int_stack = []

def isnum(num):
    try:
        int(num)
        return True
    except:
        return False
tonum = int


for x in readlines:
    if x:
        if not x.startswith(';'):
            proglines.append(x)

print('\n'.join(proglines))

def eval(statement):
    print(statement)


for line in proglines:
    for com in shlex.split(line):
        eval(com)
