import unittest

from architecture_simulator.isa.toy.toy_parser import ToyParser
from architecture_simulator.isa.toy.toy_instructions import (
    ADD,
    SUB,
    INC,
    NOP,
    DEC,
    STO,
    BRZ,
    ToyInstruction,
)
from architecture_simulator.uarch.toy.toy_architectural_state import (
    ToyArchitecturalState,
)


class TestToyParser(unittest.TestCase):
    def test_sanitize(self):
        parser = ToyParser()
        program = """ADD 0x030
        INC

        SUB    0x200
        NOP#lol
        #Zwetschgenkuchen
        DEC # Ameisenkuchen
        """
        parser.parse(program, state=ToyArchitecturalState())
        expected = [
            (1, "ADD 0x030"),
            (2, "INC"),
            (4, "SUB    0x200"),
            (5, "NOP"),
            (7, "DEC"),
        ]
        self.assertEqual(parser.sanitized_program, expected)

    def test_parse(self):
        parser = ToyParser()
        state = ToyArchitecturalState()
        program = """ADD 0x030
        INC

        SUB    0x200
        NOP#lol
        #Zwetschgenkuchen
        DEC # Ameisenkuchen
        """
        expected = [ADD(0x030), INC(), SUB(0x200), NOP(), DEC()]
        parser.parse(program=program, state=state)
        parsed = [
            ToyInstruction.from_integer(int(state.memory.read_halfword(i)))
            for i in range(len(expected))
        ]
        self.assertEqual(len(parsed), 5)
        self.assertEqual(parsed[0], expected[0])
        self.assertEqual(parsed[1], expected[1])
        self.assertEqual(parsed[2], expected[2])
        self.assertEqual(parsed[3], expected[3])
        self.assertEqual(parsed[4], expected[4])

    def test_decimal_addresses(self):
        parser = ToyParser()
        state = ToyArchitecturalState()
        program = """INC
        STO 1024
        ADD 1025
        STO 1026
        ADD 2000
        STO 4095
        SUB 1024"""

        parser.parse(program=program, state=state)
        expected = {
            0: INC(),
            1: STO(1024),
            2: ADD(1025),
            3: STO(1026),
            4: ADD(2000),
            5: STO(4095),
            6: SUB(1024),
        }
        parsed = {
            i: ToyInstruction.from_integer(int(state.memory.read_halfword(i)))
            for i in range(len(expected))
        }
        self.assertEqual(parsed, expected)

    def test_write_data(self):
        parser = ToyParser()
        state = ToyArchitecturalState()
        program = """ADD 0x400
        SUB 1025
        :1025:30
        :0x1400:0x1000F # test for overflow
        ADD 1025
        #:13141:11111"""
        parser.parse(program=program, state=state)
        self.assertEqual(state.memory.read_halfword(1025), 30)
        self.assertEqual(state.memory.read_halfword(1024), 15)
        self.assertEqual(
            ToyInstruction.from_integer(int(state.memory.read_halfword(0))), ADD(1024)
        )
        self.assertEqual(
            ToyInstruction.from_integer(int(state.memory.read_halfword(1))), SUB(1025)
        )
        self.assertEqual(
            ToyInstruction.from_integer(int(state.memory.read_halfword(2))), ADD(1025)
        )

    def test_labels(self):
        parser = ToyParser()
        state = ToyArchitecturalState()
        program = """Ameisenkuchen:
        _Apfeltarte:
        ADD Ameisenkuchen
        INC
        Banan3nkuch3n3:
        BRZ _Apfeltarte
        STO Banan3nkuch3n3"""
        parser.parse(program=program, state=state)
        expected = {0: ADD(0), 1: INC(), 2: BRZ(0), 3: STO(2)}

    def test_variables(self):
        parser = ToyParser()
        state = ToyArchitecturalState()
        program = """_test = 0x400
        test2 = 22
        INC
        sto _test
        add _test
        sto test2
        lol:
        brz lol"""
        parser.parse(program=program, state=state)
        expected = {0: INC(), 1: STO(1024), 2: ADD(1024), 3: STO(22), 4: BRZ(4)}

    def test_load_instructions(self):
        parser = ToyParser()
        state = ToyArchitecturalState()
        program = """INC
        DEC"""
        parser.parse(program, state)
        self.assertEqual(state.max_pc, 1)
        self.assertEqual(state.loaded_instruction, INC())
