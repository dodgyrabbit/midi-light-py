"""
The main beast is alive.
"""

from __future__ import print_function

import time
import animation 
import mido
from random import randint
#from lib.dotstar import Adafruit_DotStar
#from lib.Adafruit_DotStar_Pi.dotstar import Adafruit_DotStar
from lib.Mock_DotStar import Adafruit_DotStar

# How many keys there are on (your) piano/keyboard
PIANO_KEYS = 88

# The extra lights at the bottom
STATUS_LIGHTS = 32

ALL_LIGHTS = PIANO_KEYS + STATUS_LIGHTS

# The first note (far left) on your keyboard
FIRST_MIDI_NOTE = 21

def detect_usb_midi():
    """Returns the first device with USB in the name. None otherwise."""
    midi_devices = mido.Backend().get_input_names()
    first_usb_device = next((x for x in midi_devices if 'USB' in x), None)

    if first_usb_device is None:
        print("Trying name 'MIDI 1'")
        first_usb_device = next((x for x in midi_devices if 'MIDI 1' in x), None)

    return first_usb_device

def color_blend(a, b):
    """Performs a Screen blend on RGB color tuples, a and b"""
    return (255 - (((255 - a[0]) * (255 - b[0])) >> 8), 255 - (((255 - a[1]) * (255 - b[1])) >> 8), 255 - (((255 - a[2]) * (255 - b[2])) >> 8))

def main():
    """ The main loop """

    animations = []
    leds = [(0, 0, 0)] * PIANO_KEYS

    usb_device_name = detect_usb_midi()
    if usb_device_name:
        print("Opening {0} port".format(usb_device_name))
        midi_input = mido.open_input(usb_device_name)
    else:
        print("No MIDI device detected")
        midi_input = None

    print("Starting main loop...")

    if midi_input is None:
        configuration = {'mode' : 'demo'}
    else:
        configuration = {'mode' : 'midi'}

    # This overload uses SPI
    strip = Adafruit_DotStar(ALL_LIGHTS, 12000000, order='bgr')
    strip.begin()
    strip.show()

    chord = set()

    try:

        while True:

            # Apply an optional filter (default is to black out LEDs). For now, directly clear the buffer
            leds = [(0, 0, 0)] * PIANO_KEYS

            if set([0, 1, 2]).issubset(chord):
                # Reconfigure mode - set bottom pixels to RED
                for pixel in range(PIANO_KEYS, ALL_LIGHTS):
                    strip.setPixelColor(pixel, 0xFF0000)
                # TODO: Now reconfigure
                

            #for i, pixel in enumerate(leds):
            #    r, g, b = (pixel)
            #    leds[i] = (int(r/1.2), int(g/1.2), int(b/1.2))

            for current_animation in animations:
                new_frame = current_animation.get_frame()
                for i, frame_pixel in enumerate(new_frame):
                    r, g, b = (frame_pixel)
                    if r > 0:
                        leds[i] = color_blend(leds[i], frame_pixel)
            animations = [x for x in animations if not x.is_complete()]
            for i, pixel in enumerate(leds):
                r, g, b = (pixel)
                strip.setPixelColor(i, r, g, b)

            strip.show()

            # Experiment to see how long we need to sleep - it seems that this may cause problems
            # if too short
            time.sleep(0.01)

            if configuration['mode'] == 'midi':
                for message in midi_input.iter_pending():
                    print(message)
                    if message.type == 'note_on':
                        note = message.note - FIRST_MIDI_NOTE
                        chord.add(note)
                        animations.append(animation.PressureKeyPressAnimation(leds, note, message.velocity))
                    if message.type == 'note_off':
                        note = message.note - FIRST_MIDI_NOTE
                        if note in chord:
                            chord.remove(note)

            if configuration['mode'] == 'demo':
                if randint(0, 20) == 0:

                    # Here we would get a key press
                    key_pressed = randint(0, PIANO_KEYS-1)

                    animations.append(animation.PressureKeyPressAnimation(leds, key_pressed, randint(1, 192)))
                    #animations.append(animation.KeyPressAnimation(leds, key_pressed))
                    #animations.append(animation.RunLeftAnimation(leds, key_pressed))

    except KeyboardInterrupt:
        print("Exiting...")
        strip.clear()
        strip.show()
        if midi_input:
            midi_input.close()

def strand_test():
    """ Basically the same as the Adafruit stand test """

    strip = Adafruit_DotStar(ALL_LIGHTS, 12000000, order='bgr')
    strip.begin()
    strip.show()

    head = 0                                # Index of first 'on' pixel
    tail = -10                              # Index of last 'off' pixel
    color = 0xFF0000                        # 'On' color (starts red)

    counter = ALL_LIGHTS * 3 + 10
    while counter > 0:                             # Loop forever
        strip.setPixelColor(head, color)    # Turn on 'head' pixel
        strip.setPixelColor(tail, 0)        # Turn off 'tail'
        strip.show()                        # Refresh strip
        time.sleep(1.0 / 100)                # Pause 20 milliseconds (~50 fps)
        head += 1                           # Advance head position
        if head >= ALL_LIGHTS:              # Off end of strip?
            head = 0                        # Reset to start
            color >>= 8                     # Red->green->blue->black
            if color == 0:
                color = 0xFF0000            # If black, reset to red
        tail += 1                           # Advance tail position
        if tail >= ALL_LIGHTS:
            tail = 0                        # Off end? Reset
        counter -= 1


strand_test()
main()

