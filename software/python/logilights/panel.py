import sys
from struct import pack, unpack
from random import shuffle
from time import sleep, time

# Try to import logi, if we can't assume we're developing on a non BBB machine
# and force debug mode on
try:
    import logi
    DEBUG = False
except ImportError:
    DEBUG = True


DISPLAY_WIDTH = 94
DISPLAY_HEIGHT = 32

FPGA_PANEL_ADDR_REG = 0x0008
FPGA_PANEL_DATA_REG = 0x0009
FPGA_PANEL_BUFFER_REG = 0x000a

FPGA_BUFFER1_SELECT = 0x0000
FPGA_BUFFER2_SELECT = 0x0001

FPGA_BUFFER1_OFFSET = 0x0000
FPGA_BUFFER2_OFFSET = 0x2000

# 8 primary colours
COLOUR_ARRAY = {
    'BLACK'  : 0x0000,
    'WHITE'  : 0xfff,
    'RED'    : 0xf00,
    'GREEN'  : 0x0f0,
    'BLUE'   : 0x00f,
    'AQUA'   : 0x0ff,
    'PURPLE' : 0xf0f,
    'YELLOW' : 0xff0
}
COLOURS = COLOUR_ARRAY.values()


class Panel(object):
    def __init__(self, debug=False):
        self.active_buffer = 0
        self.pixel_buffer = []
        self.debug = DEBUG or debug

    def blank_display(self):
        if self.debug:
            return True

        self.pixel_buffer = []

        # Fill it with zeros
        for x in xrange(DISPLAY_HEIGHT):
            self.pixel_buffer.append([0] * DISPLAY_WIDTH)

        # Write it
        self.write_levels()

    def write_levels(self):
        if self.debug:
            return self.write_levels_debug()

        # Switch the active write buffer
        if self.active_buffer == 0:
            base = FPGA_BUFFER1_OFFSET
        else:
            base = FPGA_BUFFER2_OFFSET

        # Write the data
        for row in xrange(DISPLAY_HEIGHT):
            self.write_word(FPGA_PANEL_ADDR_REG, (base + (128 * row)))
            for col in xrange(DISPLAY_WIDTH):
                self.write_word(FPGA_PANEL_DATA_REG,
                                self.pixel_buffer[row][col])

        # Switch the active display buffer 
        if self.active_buffer == 0:
            self.write_word(FPGA_PANEL_BUFFER_REG, 0x0000)
            self.active_buffer = 1
        else:
            self.write_word(FPGA_PANEL_BUFFER_REG, 0x0001)
            self.active_buffer = 0

    def write_levels_debug(self):
        sys.stdout.write('+' + '-'*DISPLAY_WIDTH + '+\n')
        for row in xrange(DISPLAY_HEIGHT):
            sys.stdout.write('|')
            for col in xrange(DISPLAY_WIDTH):
                if self.pixel_buffer[row][col]:
                    sys.stdout.write('X')
                else:
                    sys.stdout.write(' ')
            sys.stdout.write('|\n')
        print '+' + '-'*DISPLAY_WIDTH + '+\n'

    def write_word(self, addr, word):
        logi.logiWrite(addr, self._fmt_tuple(word))

    def _fmt_tuple(self, i):
        i = (i >> 8) + ((i & 0xff) << 8)
        hi_bits = i >> 8
        lo_bits = i & 0xff
        return (hi_bits, lo_bits)


class TestPattern1(Panel):
    def first_frame(self):
        self.blank_display()

    def next_frame(self):
        global COLOURS
        self.pixel_buffer = []
        COLOURS.append(COLOURS.pop(0))
        for x in xrange(DISPLAY_HEIGHT):
            row = [COLOURS[x % len(COLOURS)]] * DISPLAY_WIDTH
            self.pixel_buffer.append(row)
        self.write_levels()


class TestPattern2(Panel):
    def first_frame(self):
        self.blank_display()

    def next_frame(self):
        global COLOURS
        self.pixel_buffer = []
        shuffle(COLOURS)
        for x in xrange(DISPLAY_HEIGHT):
            row = [COLOURS[x % len(COLOURS)]] * DISPLAY_WIDTH
            self.pixel_buffer.append(row)
        self.write_levels()


if __name__ == '__main__':
    def run60(p):
        p.first_frame()
        start = time()
        while time() < start + 60:
            p.next_frame()
            sleep(0.025)
    run60(TestPattern1())
    run60(TestPattern2())
