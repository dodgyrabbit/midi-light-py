"""
The main beast is alive.
"""

import time
from lib.Mock_DotStar import Adafruit_DotStar

# How many keys there are on (your) piano/keyboard
PIANO_KEYS = 88

# The first note (far left) on your keyboard
FIRST_MIDI_NOTE = 21

def strand_test():
    """ Basically the same as the Adafruit stand test """

    strip = Adafruit_DotStar(88)
    strip.begin()
    strip.show()

    head = 0                                # Index of first 'on' pixel
    tail = -10                              # Index of last 'off' pixel
    color = 0xFF0000                        # 'On' color (starts red)

    while True:                             # Loop forever
        strip.setPixelColor(head, color)    # Turn on 'head' pixel
        strip.setPixelColor(tail, 0)        # Turn off 'tail'
        strip.show()                        # Refresh strip
        time.sleep(1.0 / 50)                # Pause 20 milliseconds (~50 fps)
        head += 1                           # Advance head position
        if head >= PIANO_KEYS:              # Off end of strip?
            head = 0                        # Reset to start
            color >>= 8                     # Red->green->blue->black
            if color == 0:
                color = 0xFF0000            # If black, reset to red
        tail += 1                           # Advance tail position
        if tail >= PIANO_KEYS:
            tail = 0                        # Off end? Reset

strand_test()

# try:
#     while True:
#         time.sleep(1)

# except KeyboardInterrupt:
#     ## Close mock library (which should close window)
#     pass
