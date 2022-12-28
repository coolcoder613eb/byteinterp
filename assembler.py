# import os
# import sys
import argparse
'''
end    0
poke   1
peek   2
add    3
l      4
show   5
label  6
jmp    7
'''
def b(num): return bytes([num])
coms = {
    'end': b(0),
    'poke': b(1),
    'peek': b(2),
    'add': b(3),
    'l': b(4),
    'show': b(5),
    'label': b(6),
    'jmp': b(7),
    }
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
    read = f.read()
readlines1 = read.splitlines()
readlines = []
result = b''
for x in readlines1:
    if x and not x.startswith(';'):
        readlines.append(x)


for x in readlines:
    for y in x.split():
        if y.isdigit():
            if int(y) > -1 and int(y) < 256:
                result += b(int(y))
        elif y in coms:
            result += coms[y]
        elif y.startswith("'") and len(y) > 1:
            result += b(ord(y[1]))
        elif y.startswith(";"):
            break

'''
        elif y.startswith('label'):
            num = int(y.removeprefix('label'))
            result  = b(6)+b(num)+b()
'''

with open(output,'wb') as f:
    f.write(result)
print('Output:',output)
if args.showhex:
    resulthex = result.hex().upper()
    result_hex = ''
    for x in range(0,len(resulthex),2):
        result_hex += resulthex[x]+resulthex[x+1]+' '
    print('Hex:',result_hex)

