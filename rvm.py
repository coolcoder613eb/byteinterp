import sys
import os
import struct
import subprocess

class SVM:
    def __init__(self, filename):
        self.filename = filename
        self.code = self.read_file(filename)
        self.registers = [0] * 16
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 0
        self.running = True
        self.error_handler = None
        self.debug = False

    def read_file(self, filename):
        with open(filename, 'rb') as f:
            return f.read()

    def set_error_handler(self, handler):
        self.error_handler = handler

    def dump_registers(self):
        print("PC: %d SP: %d" % (self.pc, self.sp))
        for i in range(0, 16):
            print("R%d: %d" % (i, self.registers[i]))

    def run_N_instructions(self, n):
        while self.running and n > 0:
            self.run_instruction()
            n -= 1

    def run_instruction(self):
        if self.pc >= len(self.code):
            self.running = False
            return

        opcode = self.code[self.pc]
        self.pc += 1

        if opcode == 0x00:
            # HALT
            self.running = False
        elif opcode == 0x10:
            # LOAD
            reg = self.code[self.pc]
            self.pc += 1
            value = self.code[self.pc]
            self.pc += 1
            self.registers[reg] = value
        elif opcode == 0x20:
            # STORE
            reg = self.code[self.pc]
            self.pc += 1
            value = self.code[self.pc]
            self.pc += 1
            self.ram[value] = self.registers[reg]
        elif opcode == 0x30:
            # ADD
            reg1 = self.code[self.pc]
            self.pc += 1
            reg2 = self.code[self.pc]
            self.pc += 1
            self.registers[reg1] += self.registers[reg2]
        elif opcode == 0x40:
            # SUB
            reg1 = self.code[self.pc]
            self.pc += 1
            reg2 = self.code[self.pc]
            self.pc += 1
            self.registers[reg1] -= self.registers[reg2]
        elif opcode == 0x50:
            # MUL
            reg1 = self.code[self.pc]
            self.pc += 1
            reg2 = self.code[self.pc]
            self.pc += 1
            self.registers[reg1] *= self.registers[reg2]
        elif opcode == 0x60:
            # DIV
            reg1 = self.code[self.pc]
            self.pc += 1
            reg2 = self.code[self.pc]
            self.pc += 1
            self.registers[reg1] /= self.registers[reg2]
        elif opcode == 0x70:
            # JMP
            value = self.code[self.pc]
            self.pc += 1
            self.pc = value
        elif opcode == 0x80:
            # JMPZ
            reg = self.code[self.pc]
            self.pc += 1
            value = self.code[self.pc]
            self.pc += 1
            if self.registers[reg] == 0:
                self.pc = value
        elif opcode == 0x90:
            # JMPNZ
            reg = self.code[self.pc]
            self.pc += 1
            value = self.code[self.pc]
            self.pc += 1
            if self.registers[reg] != 0:
                self.pc = value
        elif opcode == 0xA0:
            # PUSH
            reg = self.code[self.pc]
            self.pc += 1
            self.ram[self.sp] = self.registers[reg]
            self.sp += 1
        elif opcode == 0xB0:
            # POP
            reg = self.code[self.pc]
            self.pc += 1
            self.sp -= 1
            self.registers[reg] = self.ram[self.sp]
        elif opcode == 0xC0:
            # CALL
            value = self.code[self.pc]
            self.pc += 1
            self.ram[self.sp] = self.pc
            self.sp += 1
            self.pc = value
        elif opcode == 0xD0:
            # RET
            self.sp -= 1
            self.pc = self.ram[self.sp]
        elif opcode == 0xE0:
            # PRINT
            reg = self.code[self.pc]
            self.pc += 1
            print(self.registers[reg])
        elif opcode == 0xF0:
            # PRINT_STACK
            value = self.code[self.pc]
            self.pc += 1
            print(self.ram[value])
        else:
            if self.error_handler:
                self.error_handler("Unknown opcode %02x" % opcode)
            else:
                print("Unknown opcode %02x" % opcode)
                self.running = False


def error(msg):
    print("ERROR running script - %s" % msg)
    sys.exit(1)


def run_file(filename, instructions):
    svm = SVM(filename)
    svm.set_error_handler(error)
    svm.run_N_instructions(instructions)
    if os.getenv("DEBUG") is not None:
        svm.dump_registers()


def main():
    if len(sys.argv) < 2:
        print("Usage: %s input-file" % sys.argv[0])
        return

    instructions = 0
    if len(sys.argv) > 2:
        instructions = int(sys.argv[2])

    run_file(sys.argv[1], instructions)


if __name__ == "__main__":
    main()
