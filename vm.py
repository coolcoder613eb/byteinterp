from collections import deque
import sys


class i:
    HALT = 0
    PUSH = 1
    ADD = 2
    SUB = 3
    MUL = 4
    DIV = 5
    NOT = 6
    AND = 7
    OR = 8
    POP = 9
    DUP = 10
    ISEQ = 11
    ISGT = 12
    JMP = 13
    JIF = 14
    LOAD = 15
    STORE = 16
    PUT = 17
    GET = 18


def get():
    try:
        # for Windows-based systems
        import msvcrt  # If successful, we are on Windows
        g = str(msvcrt.getwche())#, 'utf-8')
        #print(g, end='',flush=True)
        print([g])
        return g

    except ImportError:
        # for POSIX-based systems (with termios & tty support)
        import tty, sys, termios  # raises ImportError if unsupported

        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)

        try:
            tty.setcbreak(fd)
            answer = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
        #answer = str(answer, 'utf-8')
        print(answer, end='',flush=True)
        return answer


def test(code, debug):
    cpu = CPU(code)
    cpu.run(debug=debug)


class CPU():
    instruction = 0
    halted = False
    program = []
    var = {}

    def __init__(self, program):
        self.stack = deque()
        self.program = program

    def get_var(self, num):
        return self.var.get(num, 0)

    def set_var(self, num, val):
        self.var.update({num: val})

    def get_instruction(self):
        return self.instruction

    def get_stack(self):
        return self.stack

    def is_halted(self):
        return self.halted

    def run(self, debug=False):
        if not debug:
            while not self.halted:
                self.step()
        else:
            while not self.halted:
                print(self.stack, self.var)
                self.step()
            # print(self.stack)

    def step(self):
        if self.halted:
            raise Exception("CPU is halted!")
        else:
            nextinstr = self.get_next_word('No next instruction!')
            self.decode(nextinstr)

    def decode(self, instr):
        match instr:
            case i.HALT:
                self.halted = True
            case i.PUSH:
                value = self.get_next_word('No value after push!')
                self.stack.append(value)
            case i.ADD:
                if len(self.stack) >= 2:
                    n1 = self.stack.pop()
                    n2 = self.stack.pop()
                    self.stack.append(n1 + n2)
                else:
                    raise Exception("Not enough values on the stack!")
            case i.SUB:
                if len(self.stack) >= 2:
                    n1 = self.stack.pop()
                    n2 = self.stack.pop()
                    self.stack.append(n1 - n2)
                else:
                    raise Exception("Not enough values on the stack!")
            case i.MUL:
                if len(self.stack) >= 2:
                    n1 = self.stack.pop()
                    n2 = self.stack.pop()
                    self.stack.append(n1 * n2)
                else:
                    raise Exception("Not enough values on the stack!")
            case i.DIV:
                if len(self.stack) >= 2:
                    n1 = self.stack.pop()
                    n2 = self.stack.pop()
                    self.stack.append(n1 / n2)
                else:
                    raise Exception("Not enough values on the stack!")
            case i.NOT:
                if len(self.stack) >= 1:
                    n1 = self.stack.pop()
                    self.stack.append(int(not n1))
                else:
                    raise Exception("Not enough values on the stack!")
            case i.AND:
                if len(self.stack) >= 2:
                    n1 = self.stack.pop()
                    n2 = self.stack.pop()
                    self.stack.append(int(n1 and n2))
                else:
                    raise Exception("Not enough values on the stack!")
            case i.OR:
                if len(self.stack) >= 2:
                    n1 = self.stack.pop()
                    n2 = self.stack.pop()
                    self.stack.append(int(n1 or n2))
                else:
                    raise Exception("Not enough values on the stack!")
            case i.POP:
                if len(self.stack) >= 1:
                    n1 = self.stack.pop()
                else:
                    raise Exception("Not enough values on the stack!")
            case i.DUP:
                if len(self.stack) >= 1:
                    n1 = self.stack[-1]
                    self.stack.append(n1)
                else:
                    raise Exception("Not enough values on the stack!")
            case i.ISEQ:
                if len(self.stack) >= 2:
                    n1 = self.stack.pop()
                    n2 = self.stack.pop()
                    self.stack.append(int(n1 == n2))
                else:
                    raise Exception("Not enough values on the stack!")
            case i.ISGT:
                if len(self.stack) >= 2:
                    n1 = self.stack.pop()
                    n2 = self.stack.pop()
                    self.stack.append(int(n1 > n2))
                else:
                    raise Exception("Not enough values on the stack!")
            case i.JMP:
                n1 = self.get_next_word('No value after jmp!')
                self.instruction = n1
            case i.JIF:
                if len(self.stack) >= 1:
                    n1 = self.stack.pop()
                    n2 = self.get_next_word('No value after jmp!')
                    if n1:
                        self.instruction = n2
                else:
                    raise Exception("Not enough values on the stack!")
            case i.LOAD:
                n1 = self.get_next_word('No value after load!')
                self.stack.append(self.get_var(n1))

            case i.STORE:
                if len(self.stack) >= 1:
                    n1 = self.stack.pop()
                    n2 = self.get_next_word('No value after store!')
                    self.set_var(n2, n1)
                else:
                    raise Exception("Not enough values on the stack!")
            case i.PUT:
                if len(self.stack) >= 1:
                    n1 = self.stack.pop()
                    print(chr(n1),end='')
                else:
                    raise Exception("Not enough values on the stack!")
            case i.GET:
                while True:
                    try:
                        n1 = int(input())
                        break
                    except:
                        pass
                #print([n1])
                self.stack.append(n1)

    def get_next_word(self, errormessage):
        # print(self.stack)
        if self.instruction >= len(self.program):
            raise Exception(errormessage)
        nextword = self.program[self.instruction]
        self.instruction += 1
        return nextword

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'rb') as f:
            test(list(f.read()), False)
    else:
        print('usage: vm.py FILE')
