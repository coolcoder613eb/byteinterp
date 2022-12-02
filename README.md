# byteinterp
bytecode interpreter(sort of)
opcodes
00 exit ?
01 write the next byte to stdout
02 write a sequence of bytes to stdout until
03 end byte sequence

# easm
```
; two stacks:
; the int stack
; and the string stack
; types:
; string (in quotes): "hello world"
; integer: 3
; commands: 
; pushint push next onto int stack
; pushstr push next onto str stack
; pullint pull next from int stack
; pullstr pull next from str stack
```