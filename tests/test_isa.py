import unittest
import fixedint

from architecture_simulator.uarch.architectural_state import RegisterFile
from architecture_simulator.isa.rv32i_instructions import (
    ADD,
    SUB,
    ADDI,
    SLTI,
    SLTIU,
    XORI,
    ORI,
    ANDI,
    SLLI,
    SRLI,
    SRAI,
)
from architecture_simulator.uarch.architectural_state import ArchitecturalState

from architecture_simulator.isa.parser import riscv_bnf, riscv_parser


class TestInstructions(unittest.TestCase):
    def test_add(self):
        state = ArchitecturalState(register_file=RegisterFile(registers=[0, 5, 9, 0]))
        add_1 = ADD(rs1=1, rs2=2, rd=0)
        state = add_1.behavior(state)
        self.assertEqual(state.register_file.registers, [14, 5, 9, 0])

    def test_sub(self):
        state = ArchitecturalState(register_file=RegisterFile(registers=[0, 5, 9, 0]))
        sub_1 = SUB(rs1=1, rs2=2, rd=0)
        state = sub_1.behavior(state)
        self.assertEqual(state.register_file.registers, [-4, 5, 9, 0])

    def test_addi(self):
        state = ArchitecturalState(register_file=RegisterFile(registers=[0, 0, 0, 0]))
        addi_1 = ADDI(rd=0, rs1=0, imm=0)
        state = addi_1.behavior(state)
        addi_1 = ADDI(rd=1, rs1=3, imm=0)
        state = addi_1.behavior(state)
        self.assertEqual(state.register_file.registers, [0, 0, 0, 0])

        addi_1 = ADDI(rd=0, rs1=0, imm=1)
        state = addi_1.behavior(state)
        addi_1 = ADDI(rd=1, rs1=1, imm=2)
        state = addi_1.behavior(state)
        addi_1 = ADDI(rd=2, rs1=2, imm=3)
        state = addi_1.behavior(state)
        addi_1 = ADDI(rd=3, rs1=3, imm=4)
        state = addi_1.behavior(state)
        addi_1 = ADDI(rd=0, rs1=0, imm=9)
        state = addi_1.behavior(state)
        self.assertEqual(state.register_file.registers, [10, 2, 3, 4])

        addi_1 = ADDI(rd=0, rs1=2, imm=-4)
        state = addi_1.behavior(state)
        addi_1 = ADDI(rd=2, rs1=0, imm=-2)
        state = addi_1.behavior(state)
        self.assertEqual(state.register_file.registers, [-1, 2, -3, 4])

        maxint32 = fixedint.MutableInt32(pow(2, 32) / 2 - 1)
        minint32 = fixedint.MutableInt32(-(pow(2, 32) / 2))
        state = ArchitecturalState(
            register_file=RegisterFile(registers=[maxint32, 0, 0, 0])
        )
        addi_1 = ADDI(rd=1, rs1=0, imm=1)
        state = addi_1.behavior(state)
        self.assertEqual(state.register_file.registers, [maxint32, minint32, 0, 0])
        addi_1 = ADDI(rd=2, rs1=1, imm=-1)
        state = addi_1.behavior(state)
        self.assertEqual(
            state.register_file.registers, [maxint32, minint32, maxint32, 0]
        )
        addi_1 = ADDI(rd=3, rs1=2, imm=3)
        state = addi_1.behavior(state)
        addi_1 = ADDI(rd=1, rs1=1, imm=-3)
        state = addi_1.behavior(state)
        self.assertEqual(
            state.register_file.registers,
            [maxint32, maxint32 - 2, maxint32, minint32 + 2],
        )

    def test_andi(self):
        b0 = fixedint.MutableUInt32(0)
        b1 = fixedint.MutableUInt32(pow(2, 32) - 1)
        b2 = fixedint.MutableUInt32(3000000001)
        b3 = fixedint.MutableUInt32(2000000001)
        b4 = fixedint.MutableUInt32(839914497)

        state = ArchitecturalState(register_file=RegisterFile(registers=[b0, b1, 0, 0]))
        andi_1 = ANDI(rd=2, rs1=0, imm=0)
        state = andi_1.behavior(state)
        andi_1 = ANDI(rd=3, rs1=1, imm=0)
        state = andi_1.behavior(state)
        self.assertEqual(state.register_file.registers, [b0, b1, 0, 0])

        andi_1 = ANDI(rd=2, rs1=0, imm=1234556)
        state = andi_1.behavior(state)
        andi_1 = ANDI(rd=3, rs1=1, imm=1)
        state = andi_1.behavior(state)
        self.assertEqual(state.register_file.registers, [b0, b1, 0, 1])

        state = ArchitecturalState(register_file=RegisterFile(registers=[b2, b3, 0, 0]))
        andi_1 = ANDI(rd=0, rs1=0, imm=b2)
        state = andi_1.behavior(state)
        andi_1 = ANDI(rd=1, rs1=0, imm=b3)
        state = andi_1.behavior(state)
        andi_1 = ANDI(rd=2, rs1=0, imm=1)
        state = andi_1.behavior(state)
        self.assertEqual(state.register_file.registers, [b2, b4, 1, 0])

    def test_ori(self):
        state = ArchitecturalState(register_file=RegisterFile(registers=[0, 5, 9, 0]))

        ori_1 = ORI(rd=0, rs1=0, imm=0)
        state = ori_1.behavior(state)
        self.assertEqual(state.register_file.registers, [0, 5, 9, 0])

    def test_xori(self):
        state = ArchitecturalState(register_file=RegisterFile(registers=[0, 5, 9, 0]))

        xori_1 = XORI(rd=0, rs1=0, imm=0)
        state = xori_1.behavior(state)
        self.assertEqual(state.register_file.registers, [0, 5, 9, 0])

    def test_slli(self):
        state = ArchitecturalState(register_file=RegisterFile(registers=[0, 5, 9, 0]))

        slli_1 = SLLI(rd=0, rs1=0, imm=0)
        state = slli_1.behavior(state)
        self.assertEqual(state.register_file.registers, [0, 5, 9, 0])

    def test_srli(self):
        state = ArchitecturalState(register_file=RegisterFile(registers=[0, 5, 9, 0]))

        srli_1 = SRLI(rd=0, rs1=0, imm=0)
        state = srli_1.behavior(state)
        self.assertEqual(state.register_file.registers, [0, 5, 9, 0])

    def test_srai(self):
        state = ArchitecturalState(register_file=RegisterFile(registers=[0, 5, 9, 0]))

        srai_1 = SRAI(rd=0, rs1=0, imm=0)
        state = srai_1.behavior(state)
        self.assertEqual(state.register_file.registers, [0, 5, 9, 0])

    def test_slti(self):
        state = ArchitecturalState(register_file=RegisterFile(registers=[0, 5, 9, 0]))

        slti_1 = SLTI(rd=0, rs1=0, imm=0)
        state = slti_1.behavior(state)
        self.assertEqual(state.register_file.registers, [0, 5, 9, 0])

    def test_sltiu(self):
        state = ArchitecturalState(register_file=RegisterFile(registers=[0, 5, 9, 0]))

        sltiu_1 = SLTIU(rd=0, rs1=0, imm=0)
        state = sltiu_1.behavior(state)
        self.assertEqual(state.register_file.registers, [0, 5, 9, 0])


class TestParser(unittest.TestCase):
    program = """
add x0,x1,x2

# foo
# sub x1, x2, x4
"""
    expected = [
        ["add", ["x", "0"], ["x", "1"], ["x", "2"]],
        # ["sub", ["x", "1"], ["x", "2"], ["x", "4"]],
    ]

    def test_bnf(self):
        instr = riscv_bnf().parse_string(self.program)
        self.assertEqual(instr.as_list(), self.expected)
        self.assertNotEqual(instr[0].mnemonic, "")
        # self.assertEqual(instr[1].mnemonic, "")

    def test_parser(self):
        instr = riscv_parser(self.program)
        self.assertIsInstance(instr[0], ADD)
        self.assertEqual(instr[0].rd, 0)
        self.assertEqual(instr[0].rs1, 1)
        self.assertEqual(instr[0].rs2, 2)
        # self.assertIsInstance(instr[1], SUB)
        # self.assertEqual(instr[1].rd, 1)
        # self.assertEqual(instr[1].rs1, 2)
        # self.assertEqual(instr[1].rs2, 4)
