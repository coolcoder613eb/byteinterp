# import os
# import sys
import argparse
class i:
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
    PUT   = 17
    GET   = 18
    
def b(num): return bytes([num])

coms = {"HALT": 0,
"PUSH": 1,
"ADD": 2,
"SUB": 3,
"MUL": 4,
"DIV": 5,
"NOT": 6,
"AND": 7,
"OR": 8,
"POP": 9,
"DUP": 10,
"ISEQ": 11,
"ISGT": 12,
"JMP": 13,
"JIF": 14,
"LOAD": 15,
"STORE": 16,
"PUT": 17,
"GET": 18,}

parser = argparse.ArgumentParser()
parser.add_argument('file', help='file to assemble')
parser.add_argument('-o', '--output', help='output filename')
parser.add_argument('-s', '--showhex',action='store_true', help='output filename')
args = parser.parse_args()

file = args.file
if not args.output:
    output = '.'.join(file.split('.')[0:-1])+'.bin'
else:
    output = args.output

print('Assembling:',file)
with open(file,'r',encoding='utf-8') as f:
    read = f.read().upper()
readlines1 = read.splitlines()
readlines = []
result = b''
for x in readlines1:
    if x and not x.startswith(';'):
        readlines.append(x)


prog = []
labels = {}
for x in readlines:
    for y in x.split():
        if y.startswith(";"):
            break
        elif y.startswith(':'):
            num = y.removeprefix(':')
            labels.update({num: len(result)})

for x in readlines:
    for y in x.split():
        if y.isdigit():
            if int(y) > -1 and int(y) < 256:
                result += b(int(y))
        elif y in coms:
            result += b(coms[y])
        elif y.startswith(";"):
            break
        elif y.startswith(':'):
            num = y.removeprefix(':')
            labels.update({num:len(result)})
            #result  = b(6)+b(num)+b()
        elif y.startswith('+'):
            num = y.removeprefix('+')
            result += b(labels[num])

with open(output,'wb') as f:
    f.write(result)
print('Output:',output)
if args.showhex:
    resulthex = result.hex().upper()
    result_hex = ''
    for x in range(0,len(resulthex),2):
        result_hex += resulthex[x]+resulthex[x+1]+' '
    print('Hex:',result_hex)

