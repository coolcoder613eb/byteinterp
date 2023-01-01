; will output "A"
; poke 50 add l 60 l 5
; show peek
; show add l 60 l 5
push 60
push 5
add
put
push 0
store 0
:h
get
put
load 0
push 1
add
store 0
jmp +h
:endh
halt