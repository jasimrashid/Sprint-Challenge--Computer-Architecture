"""CPU functionality."""

import sys

#TODO: use 
op_LDI = 0b10000010
op_PRN = 0b01000111
op_HLT = 0b00000001
op_MUL = 0b10100010
op_ADD = 0b10100000
op_PUSH = 0b01000101
op_POP = 0b01000110
op_CALL = 0b01010000
op_RET = 0b00010001
op_CMP = 0b10100111
op_JEQ = 0b01010101
op_PRA = 0b01001000
op_LD = 0b10000011
op_INC = 0b01100101
op_DEC = 0b01100110
op_JMP = 0b01010100
op_JNE = 0b01010110
op_AND_OP = 0b10101000
op_OR_OP = 0b10101010

class CPU:
    """Main CPU class."""

    def __init__(self): #TODO
        """Construct a new CPU."""
        self.pc = None #PROGRAM COUNTER
        ir = None
        self.ram = [None] * 256
        self.reg = [None] * 8
        self.FL = [0] * 8
        IM = 5
        IS = 6
        self.SP = 7
        self.reg[self.SP] = 0xF4 #Initialie SP
        self.running = None #TODO refactor
        self.branchtable = {}
        self.branchtable[op_LDI] = self.ldi
        self.branchtable[op_PRN] = self.prn
        self.branchtable[op_HLT] = self.hlt
        self.branchtable[op_ADD] = self.add
        self.branchtable[op_MUL] = self.mul
        self.branchtable[op_PUSH] = self.push
        self.branchtable[op_POP] = self.pop
        self.branchtable[op_CALL] = self.call
        self.branchtable[op_RET] = self.ret
        self.branchtable[op_CMP] = self.cmp
        self.branchtable[op_JEQ] = self.jeq
        self.branchtable[op_LD] = self.ld
        self.branchtable[op_PRA] = self.pra
        self.branchtable[op_INC] = self.inc
        self.branchtable[op_DEC] = self.dec
        self.branchtable[op_JMP] = self.jmp
        self.branchtable[op_JNE] = self.jne
        self.branchtable[op_AND_OP] = self.and_op
        self.branchtable[op_OR_OP] = self.or_op
        
        

    def load_hardcoded(self):
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    
    def load(self, load_file):
        """Load a program into memory."""

        address = 0

        try:
            address = 0

            with open(load_file) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()

                    if n == '':
                        continue

                    try:
                        n = int(n,2)
                    except ValueError:
                        print(f"Invalid number '{n}''")
                        sys.exit(1)

                    self.ram[address] = n
                    address += 1

        except FileNotFoundError:
            print(f"File not found: '{load_file}'")
            sys.exit(2)


    def call(self):

        self.ram_write(self.reg[self.SP],self.pc+2)

        self.pc = self.reg[self.ram_read(self.pc+1)]

    def cmp(self):
        if self.pc == 25:
            breakpoint()
        if self.reg[self.ram_read(self.pc+1)] > self.reg[self.ram_read(self.pc+2)]:
            self.FL[5] = 1
        elif self.reg[self.ram_read(self.pc+1)] < self.reg[self.ram_read(self.pc+2)]:
            self.FL[6] = 1
        else:
            self.FL[7] = 1
        self.pc += 3

    def dec(self):
        self.reg[self.ram_read(self.pc+1)] -= 1
        self.pc += 2
    
    def inc(self):
        self.reg[self.ram_read(self.pc+1)] += 1
        self.pc += 2

    
    def jeq(self):
        if self.FL[7] == 1:
            self.pc = self.reg[self.ram_read(self.pc+1)]
        else:
            self.pc +=2


    def jmp(self):
        self.pc = self.reg[self.ram_read(self.pc+1)]

    def jne(self):
        if self.FL[7] == 0:
            self.pc = self.reg[self.ram_read(self.pc+1)]
        else:
            self.pc += 2



        
    def ret(self):
        self.pc = self.ram_read(self.reg[self.SP])

        self.reg[self.SP] += 1

    

    def alu(self, op, reg_a, reg_b=None):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = 255 - self.reg[reg_a] #test
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
        

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ld(self):
        self.reg[self.ram[self.pc+1]] = self.reg[self.ram[self.pc+2]]
        self.pc += 3

    def ldi(self):
        
        self.reg[self.ram_read(address = self.pc + 1)] = self.ram_read(address=self.pc+2)
        self.pc += 3

    def pra(self):
        val = self.reg[self.ram_read(self.pc+1)]
        print(chr(val-32))
        self.pc += 2
    
    def prn(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def hlt(self):
        self.running = False

    def mul(self):
        self.alu(op='MUL',reg_a=self.ram_read(self.pc+1),reg_b=self.ram_read(self.pc+2))
        self.pc += 3

    def add(self):
        self.alu(op='ADD',reg_a=self.ram_read(self.pc+1),reg_b=self.ram_read(self.pc+2))
        self.pc += 3

    def and_op(self):
        # bitwise-AND the value in two registers and store the result in registerA.
        self.alu(op='AND',reg_a=self.ram_read(self.pc+1),reg_b=self.ram_read(self.pc+2))
        self.pc += 3

    def not_op(self):
        self.alu(op='OR',reg_a=self.ram_read(self.pc+1))
        self.pc += 2


    def or_op(self):
        self.alu(op='OR',reg_a=self.ram_read(self.pc+1),reg_b=self.ram_read(self.pc+2))
        self.pc += 3

    def shr(self):
        self.alu(op='SHR',reg_a=self.ram_read(self.pc+1),reg_b=self.ram_read(self.pc+2))
        self.pc += 3

    def shl(self):
        self.alu(op='SHL',reg_a=self.ram_read(self.pc+1),reg_b=self.ram_read(self.pc+2))
        self.pc += 3

    def xor(self):
        self.alu(op='XOR',reg_a=self.ram_read(self.pc+1),reg_b=self.ram_read(self.pc+2))
        self.pc += 3
        
        
    def push(self):
        self.reg[self.SP] -= 1
        value = self.reg[self.ram[self.pc+1]]
        self.ram_write(address = self.reg[self.SP], value=value )
        self.pc += 2

    def pop(self):
        value = self.ram[self.reg[self.SP]]
        self.reg[self.ram[self.pc + 1]] = value

        self.reg[self.SP] += 1
        self.pc += 2

    def run(self): #TODO
        """Run the CPU."""
        self.running = True
        self.pc = 0

        while self.running:
            ir = self.ram[self.pc]

            try:
                self.branchtable[ir]()
            except Exception:
                print(f"Unknown instruction")



    def ram_read(self, address): #TODO
        """ 
        should accept the address to read and return the value stored there.
        """
        if  0 <= address <= 255:
            return self.ram[address]
        else:
            print('Invalid address')
            return None

    def ram_write(self, address,value): #TODO
        self.ram[address] = value
