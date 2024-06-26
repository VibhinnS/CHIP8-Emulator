import pyglet
import sys
import logging
from opcodes import Opcodes

class CHIP8(pyglet.window.Window):
    """Pyglet window for CHIP-8 emulator - pyglet does not support threads"""
    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    memory = [0] * 4960  # 4096 bytes of memory
    display_buffer = [0] * 32 * 64  # 64x32 display buffer
    register_bank = [0] * 16  # 16 8-bit registers
    sound_timer = 0  # sound timer
    delay_timer = 0  # delay timer
    index = 0  # 16 bit index register
    pc = 0  # 16 bit program counter
    stack :list[str]= []  # stack pointer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opcodes = Opcodes(self)

    def main(self) -> None:
        self.initialize()
        self.load_rom(sys.argv[1])
        while not self.has_exit:
            self.cycle()
            self.draw()

    def initialize(self) -> None:
        self.clear()
        self.memory = [0]*4096
        self.register_bank = [0]*16
        self.display_buffer = [0]*32*64
        self.stack = []
        self.Key_inputs = [0]*16
        self.opcode = 0
        self.index = 0

        self.delay_timer = 0
        self.sound_timer = 0
        self.should_draw = False

        self.pc = 0x200

        i :int = 0
        while i < 80:
            #char-80 fontset for CHIP-8
            self.memory[i] = self.chip8_fontset[i]
            i += 1

    def load_rom(self, ROM_PATH) -> None:
        """Loading ROM in the memory as a binary file"""
        logging.log(logging.INFO, "Loading ROM: %s", ROM_PATH)
        binary = open(ROM_PATH, "rb").read()
        i :int = 0
        while i < len(binary):
            self.memory[i + 512] = ord(binary[i])
            i += 1

    def cycle(self):
        self.opcode = self.memory[self.pc]
        self.pc += 2
        self.vx = (self.opcode & 0x0F00) >> 8
        self.vy = (self.opcode & 0x00F0) >> 4
        self.pc += 2

        # extracted_op = self.opcode & 0xf000
        # try:
        #     self.funcmap[extracted_op]()
        # except:
        #     print("Unknown opcode: %s", self.opcode)

        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
            if self.sound_timer == 0:
                print("BEEP")
                
    