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

; -------------------commands:------------------------
; pushint
; pushstr
; pullint
; pullstr
; peekint
; peekstr
; string
; int
; concat
; show
; add
; mult
; div
; exit
; intvar
; strvar

; -----------------binary commands:--------------------
; b'\x00' pushint
; b'\x01' pushstr
; b'\x02' pullint
; b'\x03' pullstr
; b'\x04' peekint
; b'\x05' peekstr
; b'\x06' string
; b'\x07' int
; b'\x08' concat
; b'\t'   show
; b'\n'   add
; b'\x0b' mult
; b'\x0c' div
; b'\r'   exit
; b'\x0e' intvar
; b'\x0f' strvar

; -----------------------docs:------------------------
; pushint push next onto int stack
; pushstr push next onto str stack
; pullint pull next from int stack
; pullstr pull next from str stack

```