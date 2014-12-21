#!/usr/bin/env python


MESSAGES = [
    ['fonts/HARNGTON.TTF', 'YELLOW', 'Seasons', 'YELLOW', 'Greetings', None],
    ['fonts/OLDENGL.TTF', 'RED', 'Merry', 'GREEN', 'Christmas', None],
    ['fonts/COOPBL.TTF', 'BLUE', 'Joyeux', 'YELLOW', 'Noel', None],
    ['fonts/yataghan.ttf', 'AQUA', 'Feliz', 'PURPLE', 'Navidad', None],
    ['fonts/HARNGTON.TTF', 'GREEN', 'Sheng Dan', 'RED', 'Kuai Le', None],
    ['fonts/RAVIE.TTF', 'PURPLE', 'Wesolych', 'BLUE', 'Swiat', None],
]


import sys
import os, os.path
from time import sleep

from logilights.font import Font
from logilights.panel import COLOUR_ARRAY, DISPLAY_HEIGHT, DISPLAY_WIDTH
from logilights.panel import Panel


class TwoLineText(Panel):
    def __init__(self, *args, **kwargs):
        super(TwoLineText, self).__init__(*args, **kwargs)

    def render_message(self, font_file, colour1, text1, colour2, text2, prerendered):
        global MESSAGES

        # If the frame has been pre-rendered, just show it
        if prerendered:
            self.pixel_buffer = prerendered
            self.write_levels()
            return True

        # Blank the screen
        self.pixel_buffer = []
        for row in xrange(DISPLAY_HEIGHT):
            self.pixel_buffer.append([0]*DISPLAY_WIDTH)

        # Determine the location of the font file, so we don't have to specify
        # the full path above
        font_file = os.path.join(os.path.dirname(__file__), font_file)

        # Determine best font size to use
        font1 = self.calculate_font(font_file, text1, DISPLAY_HEIGHT/2)
        font2 = self.calculate_font(font_file, text2, DISPLAY_HEIGHT/2)
        self.fnt = Font(font_file,  min([font1, font2]))

        # Render line 1
        self.render_line(0, COLOUR_ARRAY.get(colour1, 'RED'), text1)

        # Render line 2
        self.render_line(16, COLOUR_ARRAY.get(colour2, 'RED'), text2)

        # Save the current frame to the prerender spot in the first MESSAGE
        MESSAGES[0][5] = self.pixel_buffer

        # Write Levels
        self.write_levels()

    def calculate_font(self, font_file, text, size):
        fnt = Font(font_file, size)
        data = fnt.render_text(text)
        if data.height > (DISPLAY_HEIGHT / 2) or data.width > DISPLAY_WIDTH:
            size = self.calculate_font(font_file, text, size-1)
        return size

    def render_line(self, offset, colour, text):
        data = self.fnt.render_text(text)
        gap_above = int((DISPLAY_HEIGHT/2 - data.height) / 2)
        for row in range(data.height):
            row_num = row + offset + gap_above
            gap_left = int((DISPLAY_WIDTH - data.width) / 2)
            row_start = row * data.width
            row_end = row_start + DISPLAY_WIDTH
            pixels = data.pixels[row_start:row_end]
            for col in xrange(data.width):
                if pixels[col]:
                    self.pixel_buffer[row_num][gap_left+col] = colour
        

if __name__ == '__main__':
    p = TwoLineText()
    while True:
        p.render_message(*MESSAGES[0])
        MESSAGES.append(MESSAGES.pop(0))
        sleep(5)
