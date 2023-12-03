from enum import Enum


class Opcodes(Enum):
    # Calculations
    ADD = 0x00
    ADDI = 0x80
    AND = 0x01
    ANDI = 0x81
    # ...

    # Jumps
    IFEQ = 0x20
    IFNE = 0x21
    # unsigned (default)
    # IFL: 0x22
    # IFLE: 0x23
    # IFG: 0x24
    # IFGE: 0x25
    # # signed
    # IFLS: 0x26
    # IFLES: 0x27
    # IFGS: 0x28
    # IFGES: 0x29

    # Other
    # load from and save to RAM
    LOAD = 0x30
    SAVE = 0x31


class Addresses(Enum):
    REG0 = 0x00
    REG1 = 0x01
    REG2 = 0x02
    REG3 = 0x03
    REG4 = 0x04
    REG5 = 0x05
    PC = 0x06
    IO = 0x07


class LEG:
    """
    MSB
    IM_ARG_1  IM_ARG_2  ...

    0 - 31: Calculation
    32 - 48: Jumps
    49, 50: Load, Save

    Binary
    ======

    MSB                         LSB
    128     64      32      16      8       4       2       1
    --------------------------------------------------------------
                                    <From 0 to F>
                            1
                    2,3
            4,5,6,7
    8,9,A,B,C,D,E,F
    """

    def __init__(self, program: list[int], input: list[int], output: list[int]):
        self.program = program  # 8 bit RAM
        self.input = input
        self.output = output

        self.ram = [0] * 255  # 8 bit RAM
        self.stack = [0] * 255  # 8 bit RAM

        self.registers = {
            Addresses.REG0: 0,
            Addresses.REG1: 0,
            Addresses.REG2: 0,
            Addresses.REG3: 0,
            Addresses.REG4: 0,
            Addresses.REG5: 0,
            Addresses.PC: 0,
        }

        self._opcodes = {
            Opcodes.ADD: self._op_add,
            Opcodes.ADDI: self._op_addi,
            Opcodes.AND: self._op_and,
            Opcodes.ANDI: self._op_andi,
            # ...
            Opcodes.IFEQ: self._op_ifeq,
        }

        self._jumping = False

    #
    # Clock
    #
    def tick(self):
        opcode, arg1, arg2, arg3 = self._read_program()
        self._apply(opcode, arg1, arg2, arg3)
        if not self._jumping:
            self.registers[Addresses.PC] = (self.registers[Addresses.PC] + 4) % 255
        else:
            self._jumping = False

    def _read_program(self):
        pc = self.registers[Addresses.PC]
        opcode = self.program[pc]
        arg1, arg2, arg3 = (
            self.program[pc + 1],
            self.program[pc + 2],
            self.program[pc + 3],
        )
        return opcode, arg1, arg2, arg3

    def _apply(self, opcode: int, arg1: int, arg2: int, arg3: int):
        if opcode in self._opcodes:
            op = self._opcodes[opcode]
            op(arg1, arg2, arg3)

    #
    # ALU
    #
    def _op_add(self, arg1_reg: int, arg2_reg: int, res_reg: int):
        a = self._get(arg1_reg)
        b = self._get(arg2_reg)
        res = (a + b) % 255
        self._set(res_reg, res)

    def _op_addi(self, arg1_reg: int, arg2_im: int, res_reg: int):
        a = self._get(arg1_reg)
        b = arg2_im
        res = (a + b) % 255
        self._set(res_reg, res)

    def _op_and(self, arg1_reg: int, arg2_reg: int, res_reg: int):
        a = self._get(arg1_reg)
        b = self._get(arg2_reg)
        res = a & b
        self._set(res_reg, res)

    def _op_andi(self, arg1_reg: int, arg2_im: int, res_reg: int):
        a = self._get(arg1_reg)
        b = arg2_im
        res = a & b
        self._set(res_reg, res)

    # ...

    #
    # Jumps
    #

    def _op_ifeq(self, arg1_reg: int, arg2_reg: int, jump_addr: int):
        a = self._get(arg1_reg)
        b = self._get(arg2_reg)
        if a == b:
            self.registers[Addresses.PC] = jump_addr
            self._jumping = True

    # ...

    #
    # Helpers
    #
    def _get(self, arg: int) -> int:
        if arg in self.registers:
            reg = self.registers[arg]
            return reg
        if arg == Addresses.IO:
            return 0  # TODO, stream
        return 0

    def _set(self, arg: int, value: int):
        if arg in self.registers:
            self.registers[arg] = value
        if arg == Addresses.IO:
            pass
        return 0

    def print_debug(self):
        print(self.registers)
        # print(self.registers[Addresses.PC])


if __name__ == "__main__":
    # fmt: off
    program = [
        Opcodes.ADDI, Addresses.REG0, 0x10101010, Addresses.REG0,               # 0, 3
        Opcodes.ADDI, Addresses.REG1, 10, Addresses.REG1,               # 4, 7
        Opcodes.AND, Addresses.REG0, Addresses.REG1, Addresses.REG2,    # 8, 11
        Opcodes.IFEQ, Addresses.REG2, Addresses.REG2, 0x00,              # 12, 15
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
    ]
    # fmt: on
    input, output = None, None
    leg = LEG(program, input, output)
    leg.print_debug()

    for i in range(20):
        leg.tick()
        leg.print_debug()
