#!/usr/bin/env python

import sys
from time import sleep

from logilights.font import Font
from logilights.panel import COLOUR_ARRAY, DISPLAY_HEIGHT, DISPLAY_WIDTH
from logilights.panel import Panel


class ScrollingText(Panel):
    def __init__(self, colour, font_file, text, *args, **kwargs):
        super(ScrollingText, self).__init__(*args, **kwargs)
        self.colour = COLOUR_ARRAY[colour]
        self.offset = 0
        self.calculate_font(font_file, text, size=DISPLAY_HEIGHT)

    def calculate_font(self, font_file, text, size):
        self.fnt = Font(font_file, size)
        num_spaces = (DISPLAY_WIDTH / self.fnt.render_text(' ').width) + 1
        self.data = self.fnt.render_text(' ' * num_spaces + text + ' ' * num_spaces)
        if self.data.height > DISPLAY_HEIGHT:
            self.calculate_font(font_file, text, size-1)

    def first_frame(self):
        self.blank_display()
        self.pixel_buffer = self.get_viewport()
        self.write_levels()

    def next_frame(self):
        if not self.slide_viewport(1):
            sys.exit(0)
        self.pixel_buffer = self.get_viewport()
        self.write_levels()

    def get_viewport(self):
        gap_above = int((DISPLAY_HEIGHT - self.data.height) / 2)
        gap_below = DISPLAY_HEIGHT - gap_above - self.data.height
        tmp_buffer = []
        for row in xrange(gap_above):
            tmp_buffer.append([0] * DISPLAY_WIDTH)
        for row in xrange(self.data.height):
            tmp_buffer.append([0] * DISPLAY_WIDTH)
            row_start = row * self.data.width
            row_end = row_start + DISPLAY_WIDTH
            pixels = self.data.pixels[self.offset+row_start:self.offset+row_end]
            for col in xrange(DISPLAY_WIDTH):
                if pixels[col]:
                    tmp_buffer[row+gap_above][col] = self.colour
        for row in xrange(gap_below):
            tmp_buffer.append([0] * DISPLAY_WIDTH)
        return tmp_buffer

    def slide_viewport(self, amount=1):
        if self.offset == self.data.width - DISPLAY_WIDTH:
            return False
        self.offset += amount
        return True


if __name__ == '__main__':
    p = ScrollingText(sys.argv[1], sys.argv[2], ' '.join(sys.argv[3:]))
    p.first_frame()
    while True:
        p.next_frame()
