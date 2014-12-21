#!/usr/bin/env python

TARGET_DATE = [2014, 12, 25]
EVENT_NAME = ['SLEEP', 'LEFT']

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
        self.font_cache = {}
        self.font_file = font_file

    def render_panel(self):

        # Build the pixel buffer big enough for the screren
        self.pixel_buffer = []
        for row in xrange(DISPLAY_HEIGHT):
            self.pixel_buffer.append([0]*DISPLAY_WIDTH)

        # Calculate how many days remaining until the target date
        days_remaining = str((datetime(*TARGET_DATE) - datetime.today()).days)

        # Pluralise firt word of event name
        if int(days_remaining) != 1 and EVENT_NAME[0][-1] != 'S':
            EVENT_NAME[0] += 'S'

        # Determine the size for the fonts
        self.calculate_font(days_remaining, key='counter', rows=1)
        for word in EVENT_NAME:
            self.calculate_font(word, key='event_name', rows=2)

        # Indent from the left edge of the screen
        h_offset = 5

        # Render number of days remaining
        rendered = self.render_text(days_remaining, h_offset, 0, 'counter', COLOUR_ARRAY['RED'], 1)
        h_offset += rendered.width + 1

        # Render the event name
        v_offset = 2
        for word in EVENT_NAME:
            rendered = self.render_text(word, h_offset, v_offset, 'event_name', COLOUR_ARRAY['GREEN'], 2)
            v_offset += rendered.height + 1

        # Write Levels
        self.write_levels()

    def calculate_font(self, text, key, rows, size=None, font_file=None):
        if font_file is None:
            font_file = self.font_file
        if size is None:
            size = DISPLAY_HEIGHT / rows
        fnt = Font(font_file, size)
        data = fnt.render_text(text)
        if data.height > (DISPLAY_HEIGHT / rows) or data.width > DISPLAY_WIDTH:
            size = self.calculate_font(text, key, rows, size-1)
        self.font_cache[key] = fnt

    def render_text(self, text, h_offset, v_offset, key, colour, rows):
        data = self.font_cache[key].render_text(text)
        gap_above = int((DISPLAY_HEIGHT/rows - data.height) / 2)
        # If h_offset is negative, we're aligning on the right edge
        if h_offset < 0:
            h_offset = DISPLAY_WIDTH - data.width - abs(h_offset)
        for row in xrange(data.height):
            row_num = row + v_offset + gap_above
            row_start = row * data.width
            pixels = data.pixels[row_start:row_start+data.width]
            for col in xrange(data.width):
                if pixels[col]:
                    self.pixel_buffer[row_num][h_offset+col] = colour
        return data


if __name__ == '__main__':
    p = DaysToGoText(debug=True)
    while True:
        p.render_panel()
        sleep(1)