#!/usr/bin/env python

TARGET_DATE = [2014, 12, 25]
EVENT_NAME = ['SLEEP', 'LEFT']

ROWS_COUNTER = 1
ROWS_EVENT = 2
ROWS_DATETIME = 4

import sys
import os, os.path
from datetime import datetime
from time import sleep

from logilights.font import Font
from logilights.panel import COLOUR_ARRAY, DISPLAY_HEIGHT, DISPLAY_WIDTH
from logilights.panel import Panel


font_file = os.path.join(os.path.dirname(__file__),
                         'fonts', 'special-elite.ttf')
font_file2 = os.path.join(os.path.dirname(__file__),
                         'fonts', '5x7-practical.ttf')


class DaysToGoText(Panel):
    def __init__(self, *args, **kwargs):
        super(DaysToGoText, self).__init__(*args, **kwargs)
        self.font_cache = {}
        self.font_file = font_file
        self.show_colon = True

    def render_panel(self):

        # Build the pixel buffer big enough for the screren
        self.pixel_buffer = []
        for row in xrange(DISPLAY_HEIGHT):
            self.pixel_buffer.append([0]*DISPLAY_WIDTH)

        # Calculate how many days remaining until the target date
        days_remaining = str((datetime(*TARGET_DATE) - datetime.today()).days+1)
        current_date = datetime.now().strftime('%d-%m')
        current_time = datetime.now().strftime('%H:%M')

        # Pluralise firt word of event name
        if int(days_remaining) != 1 and EVENT_NAME[0][-1] != 'S':
            EVENT_NAME[0] += 'S'

        # Determine the size for the fonts
        self.calculate_font(days_remaining, key='counter', rows=ROWS_COUNTER)
        for word in EVENT_NAME:
            self.calculate_font(word, key='event_name', rows=ROWS_EVENT)
        self.calculate_font(current_time, key='date_time', rows=1, size=16, font_file=font_file2)
        self.calculate_font(current_time, key='date_time', rows=1, size=16, font_file=font_file2)

        # Indent from the left edge of the screen
        h_offset = 5

        # Render number of days remaining
        rendered = self.render_text(days_remaining, h_offset, 0, 'counter', COLOUR_ARRAY['RED'], ROWS_COUNTER)
        h_offset += rendered.width + 1

        # Render the event name
        v_offset = 2
        for word in EVENT_NAME:
            rendered = self.render_text(word, h_offset, v_offset, 'event_name', COLOUR_ARRAY['GREEN'], ROWS_EVENT)
            v_offset += rendered.height + 1

        # Render the current date time
        rendered1 = self.render_text(current_time, -1, -1, 'date_time', COLOUR_ARRAY['YELLOW'], ROWS_DATETIME)
        rendered2 = self.render_text(current_date, -1, -1-rendered1.height-1, 'date_time', COLOUR_ARRAY['YELLOW'], ROWS_DATETIME)

        # Blank out the dots in the time every second refresh
        # Do this be redrawing the last 3 characters of the time in black and
        # then the last two characters in yellow again
        if self.show_colon:
            self.render_text(current_time[2:], -1, -1, 'date_time', COLOUR_ARRAY['BLACK'], ROWS_DATETIME)
            self.render_text(current_time[3:], -1, -1, 'date_time', COLOUR_ARRAY['YELLOW'], ROWS_DATETIME)
        self.show_colon = not self.show_colon

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
            h_offset = DISPLAY_WIDTH - data.width - abs(h_offset) + 1
        if v_offset < 0:
            v_offset = DISPLAY_HEIGHT - data.height - abs(v_offset) + 1
        for row in xrange(data.height):
            row_num = row + v_offset + gap_above
            row_start = row * data.width
            pixels = data.pixels[row_start:row_start+data.width]
            for col in xrange(data.width):
                if pixels[col]:
                    self.pixel_buffer[row_num][h_offset+col] = colour
        return data


if __name__ == '__main__':
    p = DaysToGoText()
    while True:
        p.render_panel()
        sleep(1)
