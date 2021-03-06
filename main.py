"""
The main midi-light-pi module.
"""

from __future__ import print_function
from __future__ import division

import time
from random import randint
import animation
import timer

import mido

#import sys
#print(sys.path)

# Dynamically decide if we use the emulator or an actual DotStar.
try:
    from dotstar import Adafruit_DotStar
    # On RPI use this line instead
    # from dotstar import Adafruit_DotStar
except ImportError:
    print("Loading UI instead of Adafruit_DotStar_Pi")
    from Mock_DotStar import Adafruit_DotStar

# How many keys there are on (your) piano/keyboard
PIANO_KEYS = 88

# The extra lights at the bottom
STATUS_LIGHTS = 32

ALL_LIGHTS = PIANO_KEYS + STATUS_LIGHTS

# The first note (far left) on your keyboard
FIRST_MIDI_NOTE = 21

# pylint: disable=C0326
GAMMA = [ \
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,\
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,\
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,\
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,\
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,\
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,\
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,\
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,\
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,\
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,\
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,\
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,\
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,\
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,\
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,\
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 ]

# TODO: Need to refactor this main module into it's own class
configuration = {}
# This overload uses SPI
STRIP = Adafruit_DotStar(ALL_LIGHTS, 12000000, order='bgr')

def detect_midi_device():
    """Returns the a MIDI device name. Looks for devices starting with 'USB', 'MIDI 1' or 'VMPK'.
    None otherwise.
    """
    midi_devices = []
    try:
        # Override default (portmidi) to use rtmidi. Note that portmidi
        # worked fine on RPI but rtmidi is faster and more portable in my experience
        # rtmidi had to be built directly on the RPI though
        mido.set_backend('mido.backends.rtmidi')
        midi_devices = mido.get_input_names()

    except ImportError:
        print("Could not load rtmidi. Try 'pip install python-rtmidi'")

    first_usb_device = next((x for x in midi_devices if 'USB' in x), None)

    if first_usb_device is None:
        print("Trying name 'MIDI 1'")
        first_usb_device = next((x for x in midi_devices if 'MIDI 1' in x), None)

    if first_usb_device is None:
        print("Trying name VMPK")
        first_usb_device = next((x for x in midi_devices if 'VMPK' in x), None)

    return first_usb_device

def color_blend(color_a, color_b):
    """Performs a Screen blend on RGB color tuples, a and b"""
    return (255 - (((255 - color_a[0]) * (255 - color_b[0])) >> 8), \
            255 - (((255 - color_a[1]) * (255 - color_b[1])) >> 8), \
            255 - (((255 - color_a[2]) * (255 - color_b[2])) >> 8))

def draw_status(color):
    """Draws the status lights underneath the light bar"""
    if not color is None:
        # Adjust brightness
        r, g, b = ((color >> 16) & 255, (color >> 8) & 255, color & 255)
        r = int(r * (configuration['status_brightness'] / 255))
        b = int(b * (configuration['status_brightness'] / 255))
        g = int(g * (configuration['status_brightness'] / 255))
        color = b + (g << 8) + (r << 16)
        for pixel in range(PIANO_KEYS, ALL_LIGHTS):
            STRIP.setPixelColor(pixel, color)

def main():
    """ The main loop """
    status_color = None

    animations = []
    leds = [(0, 0, 0)] * PIANO_KEYS

    usb_device_name = detect_midi_device()
    if usb_device_name:
        print("Opening {0} port".format(usb_device_name))
        midi_input = mido.open_input(usb_device_name)
    else:
        print("No MIDI device detected")
        midi_input = None

    print("Starting main loop...")

    configuration['mode'] = 'demo'
    configuration['gamma_correction'] = False
    configuration['animation'] = 1
    configuration['demo_delay'] = 60 * 5
    configuration['demo_done'] = 60 * 60
    configuration['status_brightness'] = 255

    # Start in demo on startup
    last_key_time = time.time() - configuration['demo_delay']

    STRIP.begin()
    STRIP.show()

    # Used to detect the "secret chord" for controlling various aspects
    chord = set()

    #running_animation = animation.RunningAnimation(PIANO_KEYS)
    #animations.append(running_animation)
    practice_timer = timer.Timer()
    animations.append(practice_timer)
    #animations.append(animation.BeatAnimation(44, 80))

    try:

        while True:
            idle_time = time.time() - last_key_time
            if idle_time > configuration['demo_done']:
                if configuration['mode'] != 'sleep':
                    configuration['mode'] = 'sleep'
                    status_color = 0x000000
                    STRIP.clear()
                    STRIP.show()
            elif idle_time > configuration['demo_delay']:
                if configuration['mode'] != 'demo':
                    configuration['mode'] = 'demo'
                    # Hide "forever" while in demo mode. TODO: Improve with special case.
                    practice_timer.hide(1000 * 60 * 60 * 24 * 365)
            elif configuration['mode'] != 'midi':
                configuration['mode'] = 'midi'

            # Apply an optional filter (default is to black out LEDs).
            # For now, directly clear the buffer.
            leds = [(0, 0, 0)] * PIANO_KEYS

            if set([0, 1]).issubset(chord):
                print("Secret chord pressed")

                if 2 in chord:
                    print("Red status lights")
                    status_color = 0xFF0000
                if 3 in chord:
                    status_color = 0x00FF00
                if 4 in chord:
                    status_color = 0x0000FF
                if 5 in chord:
                    status_color = 0xFFFFFF
                if 6 in chord:
                    status_color = 0xFFFC7F
                if 7 in chord:
                    status_color = 0x000000

                draw_status(status_color)

                # 15 is the second C note from the left. Toggle brightness down.
                if 15 in chord:
                    configuration['status_brightness'] -= 1
                    if configuration['status_brightness'] < 1:
                        configuration['status_brightness'] = 1
                    draw_status(status_color)
                # 16 is the second D note from the left. Toggle brightness up.
                if 17 in chord:
                    configuration['status_brightness'] += 1
                    if configuration['status_brightness'] > 255:
                        configuration['status_brightness'] = 255
                    draw_status(status_color)

                if 14 in chord:
                    practice_timer.restart()

            #for i, pixel in enumerate(leds):
            #    r, g, b = (pixel)
            #    leds[i] = (int(r/1.2), int(g/1.2), int(b/1.2))

            for current_animation in animations:
                new_frame = current_animation.get_frame()
                for i, frame_pixel in enumerate(new_frame):
                    r, g, b = (frame_pixel)
                    if r > 0 or g > 0 or b > 0:
                        leds[i] = color_blend(leds[i], frame_pixel)

            animations = [x for x in animations if not x.is_complete()]

            for i, pixel in enumerate(leds):
                r, g, b = (pixel)
                if configuration['gamma_correction']:
                    r = GAMMA[r]
                    g = GAMMA[g]
                    b = GAMMA[b]
                STRIP.setPixelColor(i, r, g, b)

            STRIP.show()

            # Experiment to see how long we need to sleep - it seems that this may cause problems
            # if too short
            time.sleep(0.01)

            if midi_input is not None:
                for message in midi_input.iter_pending():
                    print(message)
                    last_key_time = time.time()
                    practice_timer.hide(10*1000)
                    if message.type == 'note_on':
                        note = message.note - FIRST_MIDI_NOTE
                        chord.add(note)
                        #running_animation.key_pressed(message.velocity * 2)
                        animations.append(animation.PressureKeyPressAnimation(PIANO_KEYS,note, message.velocity * 2, 3000))
                        #animations.append(animation.ChristmasKeyPressAnimation(PIANO_KEYS, note, message.velocity * 2))
                        #animations.append(animation.RunLeftAnimation(note))
                        #animations.append(animation.LightUpAnimation(PIANO_KEYS, note))
                    if message.type == 'note_off':
                        note = message.note - FIRST_MIDI_NOTE
                        if note in chord:
                            chord.remove(note)

            if configuration['mode'] == 'demo':
                if randint(0, 15) == 0:

                    # Here we would get a key press
                    key_pressed = randint(0, PIANO_KEYS-1)

                    animations.append(animation.ChristmasKeyPressAnimation(PIANO_KEYS, key_pressed, randint(1, 255), 1000))
                    #animations.append(animation.PressureKeyPressAnimation(PIANO_KEYS, key_pressed, randint(1, 255), 1000))
                    #animations.append(animation.KeyPressAnimation(PIANO_KEYS, key_pressed))
                    #animations.append(animation.RunLeftAnimation(key_pressed))

    except KeyboardInterrupt:
        print("Exiting...")
        STRIP.clear()
        STRIP.show()
        STRIP.close()
        if midi_input:
            midi_input.close()

def strand_test():
    """ Basically the same as the Adafruit stand test """

    test_strip = Adafruit_DotStar(ALL_LIGHTS, 12000000, order='bgr')
    test_strip.begin()
    test_strip.show()

    head = 0                                # Index of first 'on' pixel
    tail = -10                              # Index of last 'off' pixel
    color = 0xFF0000                        # 'On' color (starts red)

    counter = ALL_LIGHTS * 3 + 10
    while counter > 0:                             # Loop forever
        test_strip.setPixelColor(head, color)    # Turn on 'head' pixel
        test_strip.setPixelColor(tail, 0)        # Turn off 'tail'
        test_strip.show()                        # Refresh strip
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


#strand_test()
main()
