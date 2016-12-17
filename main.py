"""
The main beast is alive.
"""

import time
import animation
from random import randint
from lib.Mock_DotStar import Adafruit_DotStar

# How many keys there are on (your) piano/keyboard
PIANO_KEYS = 88

# The first note (far left) on your keyboard
FIRST_MIDI_NOTE = 21


def color_blend(a, b):
    """Performs a Screen blend on RGB color tuples, a and b"""
    return (255 - (((255 - a[0]) * (255 - b[0])) >> 8), 255 - (((255 - a[1]) * (255 - b[1])) >> 8), 255 - (((255 - a[2]) * (255 - b[2])) >> 8))

def main():
    """ The main loop """

    animations = []
    leds = [(0, 0, 0)] * PIANO_KEYS

    strip = Adafruit_DotStar(PIANO_KEYS)
    strip.begin()
    strip.show()

    while True:

        # Apply an optional filter (default is to black out LEDs). For now, directly clear the buffer
        #leds = [(0, 0, 0)] * PIANO_KEYS

        for i, pixel in enumerate(leds):
            r, g, b = (pixel)
            leds[i] = (int(r/1.2), int(g/1.2), int(b/1.2))

        for current_animation in animations:
            new_frame = current_animation.get_frame()
            for i, frame_pixel in enumerate(new_frame):
                leds[i] = color_blend(leds[i], frame_pixel)

        animations = [x for x in animations if not x.is_complete]

        for i, pixel in enumerate(leds):
            r, g, b = (pixel)
            strip.setPixelColorRGB(i, r, g, b)

        strip.show()
        time.sleep(0.1)

        # Here we would get a key press
        key_pressed = randint(0,PIANO_KEYS-1)

        animations.append(animation.KeyPressAnimation(leds, key_pressed))


# Process all animations and write them into LED buffer.
# Destroy animations that are complete.
# Update the LED display.
# Process any inputs and create any new animations as needed.
# Sleep to achieve the desired frame rate.

def strand_test():
    """ Basically the same as the Adafruit stand test """

    strip = Adafruit_DotStar(PIANO_KEYS)
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

main()

# try:
#     while True:
#         time.sleep(1)

# except KeyboardInterrupt:
#     ## Close mock library (which should close window)
#     pass
