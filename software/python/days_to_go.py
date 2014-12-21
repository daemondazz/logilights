#!/usr/bin/env python

TARGET_DATE = [2014, 12, 25]

import sys
import os, os.path
from datetime import datetime
from time import sleep

from logilights.font import Font
from logilights.panel import COLOUR_ARRAY, DISPLAY_HEIGHT, DISPLAY_WIDTH
from logilights.panel import Panel


font_file = os.path.join(os.path.dirname(__file__),
                         'fonts', 'special-elite.ttf')


class DaysToGoText(Panel):
    def __init__(self, *args, **kwargs):
        super(DaysToGoText, self).__init__(*args, **kwargs)

    def render_panel(self):

        # Build the pixel buffer big enough for the screren
        self.pixel_buffer = []
        for row in xrange(DISPLAY_HEIGHT):
            self.pixel_buffer.append([0]*DISPLAY_WIDTH)

        # Calculate how many days remaining until the target date
        days_remaining = str((datetime(*TARGET_DATE) - datetime.today()).days)

        # Determine the size for the counter and render it at the left edge of the panel
        counter_size, counter_font = self.get_font(font_file, days_remaining, 1, DISPLAY_HEIGHT)
        days_string = self.render_text(counter_font, 0, 0, COLOUR_ARRAY['RED'], days_remaining)
#        h_offset = self.render_string(counter_font, 0, 0, 
#
#        # Determine best font size to use
#        font1 = self.calculate_font(font_file, text1, DISPLAY_HEIGHT/2)
#        font2 = self.calculate_font(font_file, text2, DISPLAY_HEIGHT/2)
#        self.fnt = Font(font_file,  min([font1, font2]))
#
#        # Render line 1
#        self.render_line(0, COLOUR_ARRAY.get(colour1, 'RED'), text1)
#
#        # Render line 2
#        self.render_line(16, COLOUR_ARRAY.get(colour2, 'RED'), text2)
#
#        # Save the current frame to the prerender spot in the first MESSAGE
#        MESSAGES[0][5] = self.pixel_buffer

        # Write Levels
        self.write_levels()

    def get_font(self, font_file, text, rows, size):
        fnt = Font(font_file, size)
        data = fnt.render_text(text)
        if data.height > (DISPLAY_HEIGHT / rows) or data.width > DISPLAY_WIDTH:
            size = self.calculate_font(font_file, text, rows, size-1)
        return size, fnt

    def render_text(self, font_obj, h_offset, v_offset, colour, text):
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
    p = DaysToGoText(debug=True)
    while True:
        p.render_panel()
        sleep(1)
