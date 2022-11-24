out = bytes.fromhex('01')
outseq = bytes.fromhex('02')
endseq = bytes.fromhex('03')
result = b''
for x in 'hello world':
    result+=out+bytes(x,'utf-8')

    
result+=outseq+b'/nHello World!'+endseq
result
b'\x01h\x01e\x01l\x01l\x01o\x01 \x01w\x01o\x01r\x01l\x01d\x02/nHello World!\x03'
print(result)
b'\x01h\x01e\x01l\x01l\x01o\x01 \x01w\x01o\x01r\x01l\x01d\x02/nHello World!\x03'
with open(r'C:\Users\tzema\Documents\GitHub\byteinterp\hw.bin','wb') as f:
    f.write(result)

    
38
with open(r'C:\Users\tzema\Documents\GitHub\byteinterp\hw2.bin','wb') as f:
    f.write(result)

    
38
