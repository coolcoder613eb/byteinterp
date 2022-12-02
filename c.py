out = bytes.fromhex('01')
outseq = bytes.fromhex('02')
endseq = bytes.fromhex('03')

result = b''
for x in 'hello world':
    result+=out+bytes(x,'utf-8')

    
result+=outseq+b'/nHello World!'+endseq
with open(r'C:\Users\tzema\Documents\GitHub\byteinterp\hw2.bin','wb') as f:
    f.write(result)

