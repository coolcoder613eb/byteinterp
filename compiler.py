import sys
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument('file',help='The file to compile')
parser.add_argument('-o','--output',help='output filename without extension')
args = parser.parse_args()
#print(args.file,args.output)
file = args.file
if args.output:
    outputfile = args.output
else:
    outputfile = args.file.split('.')[0]

with open(file,'r') as f:
    rfile = f.read()

with open('easm.py','r') as f:
    reasm=f.read()

reasm=reasm.replace('# --!@#$%^&*()""""""',"readlines = r'''"+rfile+"'''")
#print(r)
reasm=reasm.replace('# --!@#$%^&*()',"sys.argv.append('--!@#$%^&*()')")

if not os.path.isdir('bin'):
    os.mkdir('bin')
with open(os.path.join('bin',outputfile+'.py'),'w') as f:
    f.write(reasm)

try:
    os.chdir('bin')
    os.system('"'+sys.executable+'"'+' -m nuitka '+outputfile+'.py')

except:
    print('Error compiling!\nIs nuitka installed?')
os.chdir('..')
print(f'''
The executable produced depends on a python installation,
if you would like to make the executable 
not dependent on a python installation,
please compile {os.path.join('bin',outputfile+'.py')} with with the --standalone and --onefile options.''')