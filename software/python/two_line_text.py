#!/usr/bin/env python

import json
import numpy
import sys
import os, os.path
from time import sleep

from logilights.font import Font
from logilights.panel import COLOUR_ARRAY, DISPLAY_HEIGHT, DISPLAY_WIDTH
from logilights.panel import Panel


class TwoLineText(Panel):
    def __init__(self, messages, *args, **kwargs):
        super(TwoLineText, self).__init__(*args, **kwargs)
        self.messages = messages

    def render_message(self):

        # Split out current message
        font_file, colour1, text1, colour2, text2, prerendered = self.messages[0]

        # If the frame has been pre-rendered, just show it
        if not prerendered is None:
            self.pixel_buffer = prerendered
            self.write_levels()
            return True

        # Blank the screen
        self.pixel_buffer = self.get_blank_buffer()

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
        self.messages[0][5] = self.pixel_buffer

        # Write Levels
        self.write_levels()

    def calculate_font(self, font_file, text, size):
        fnt = Font(font_file, size)
        data = fnt.render_text(text)
        if data.height > (DISPLAY_HEIGHT / 2) or data.width >= DISPLAY_WIDTH:
            size = self.calculate_font(font_file, text, size-1)
        return size

    def render_line(self, offset, colour, text):
        # Render the line into a bytearray
        data = self.fnt.render_text(text)

        # Convert the bytearray to a numpy array
        tmp = numpy.frombuffer(data.pixels, numpy.int8)

        # Turn the numpy array into a ndarray and set pixel colours
        tmp = numpy.multiply(tmp.reshape(data.height, data.width), colour)

        # Calculate how far on the line we are shifting it (to center)
        gap_above = int((DISPLAY_HEIGHT/2 - data.height) / 2)
        gap_left = int((DISPLAY_WIDTH - data.width) / 2)

        # Overlay tmp buffer onto pixel buffer
        x1, x2 = gap_left, gap_left + data.width
        y1, y2 = offset + gap_above, offset + gap_above + data.height
        self.pixel_buffer[y1:y2,x1:x2] = tmp

    def rotate_messages(self):
        self.messages.append(self.messages.pop(0))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'ERROR: Require name of JSON file containing messages to render'
        sys.exit(1)
    with open(sys.argv[1], 'rb') as fh:
        data = json.load(fh)
    p = TwoLineText(data['messages'])
    while True:
        p.render_message()
        p.rotate_messages()
        sleep(data['sleep'])
