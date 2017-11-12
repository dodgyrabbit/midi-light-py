""" The various classes relating to animations """
from __future__ import print_function
from __future__ import division

import math

from random import randint
import time

class Animation(object):
    """The base class for any animation. An animation is a state machine that produces frames.
       Keep calling get_frame until is_complete returns true.
    """
    def __init__(self, milliseconds=None):
        """ Animation base class initializer """
        object.__init__(self)
        if milliseconds is None:
            self._milliseconds = lambda: int(round(time.time() * 1000))
        else:
            self._milliseconds = milliseconds

    def get_frame(self):
        """Return an array of tuples (r,g,b) i.e. the frame for the current state of the animation"""
        raise RuntimeError("GetFrame should only be called in derived classes")

    def is_complete(self):
        """True if this animation is complete and can be removed"""
        return False

class FireAnimation(Animation):
    """ Fire animation """
    def __init__(self):
        Animation.__init__(self)
        self._lights = []
        self._r = 255
        self._g = 255 - 40
        self._b = 40
        self._end = 0

    def get_frame(self):
        if self._milliseconds() > self._end:
            self._end = self._milliseconds() + 50
            self._lights = []
            for i in range(0, 88):
                flicker = randint(0, 150)
                r1 = self._r - flicker
                g1 = self._g - flicker
                b1 = self._b - flicker
                if r1 < 0:
                    r1 = 0
                if g1 < 0:
                    g1 = 0
                if b1 < 0:
                    b1 = 0
                self._lights.append((r1, g1, b1))
        return self._lights

    def is_complete(self):
        return False

class BeatAnimation(Animation):
    """Lights up on a specific beat"""
    def __init__(self, width, bpm, milliseconds=None):
        Animation.__init__(self, milliseconds=None)
        self._ms_per_beat = 1000 / (bpm / 60) 
        self._current_pulse_time = self._milliseconds()
        self._width = width

        # Need to step between -1.5 and 1.5
        step = 3.0 / width
        x = -1.5
        self._bell_curve = [0.0] * width

        for i, _ in enumerate(self._bell_curve):
            self._bell_curve[i] = normpdf(x, 0, 0.4)
            print(self._bell_curve[i])
            print(x)
            x += step

        print ("Beat interval {0} ".format(self._ms_per_beat))
    
    def get_frame(self):
        now = self._milliseconds()
        time_into_beat = now % self._ms_per_beat

        # Brightness decreases as time progresses into the beat. Adjust to an interval between 0-255.
        brightness = int((self._ms_per_beat - time_into_beat) / self._ms_per_beat * 256)
        pixels = [(brightness, brightness, brightness)] * self._width

        # Apply a bell curve to pixels - this avoids all of them lighting up and instead a soft ramp up and ramp down
        for i, (r, g, b) in enumerate(pixels):
            factor = self._bell_curve[i]
            pixels[i] = (int(r * factor), int(g * factor), int(b * factor))
        return pixels

    def is_complete(self):
        return False

def normpdf(x, mean, standard_deviation):
    """ Calculates the normal distribution using a probability density function
        Found it here https://stackoverflow.com/a/12413491 """
    var = float(standard_deviation)**2
    pi = 3.1415926
    denom = (2*pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

class LightUpAnimation(Animation):
    """Simple animation that lights up the given key for a short period of time"""

    def __init__(self, keys, key_pressed, duration=1000, milliseconds=None):
        """Initializes a new LightUpAnimation instance"""
        Animation.__init__(self)
        self._end = self._milliseconds() + duration
        self._leds = [(0, 0, 0)] * keys
        self._key_pressed = key_pressed

    def get_frame(self):
        """Return an array of integers representing the current state of the animation"""
        self._leds[self._key_pressed] = (255, 255, 255)
        return self._leds

    def is_complete(self):
        """True if this animation is complete and can be removed"""
        return self._milliseconds() > self._end

class PressureKeyPressAnimation(LightUpAnimation):
    """Simple animation that happens when you press a key. It is pressure sensitive."""

    def __init__(self, keys, key_pressed, velocity, duration=1000, milliseconds=None):
        """Initializes a new PressureKeyPressAnimation instance"""
        LightUpAnimation.__init__(self, keys, key_pressed, duration, milliseconds)
        self._velocity = velocity
        self._duration = duration

    def get_key_color(self):
        """Returns the color of the key pressed during animation. Override to change."""
        return (self._velocity, self._velocity, self._velocity)

    def get_frame(self):
        """Return an array of integers representing the current state of the animation."""

        time_left = self._end - self._milliseconds()
        if time_left < 0:
            time_left = 0

        r, g, b = self.get_key_color()
        fade_factor = time_left / self._duration
        r = int(r * fade_factor)
        g = int(g * fade_factor)
        b = int(b * fade_factor)

        self._leds[self._key_pressed] = (r, g, b)
        return self._leds

class RunLeftAnimation(Animation):
    """Simple animation that happens when you press a key"""

    def __init__(self, key_pressed):
        """Initializes a new KeyPressAnimation instance"""
        Animation.__init__(self)
        self._key_pressed = key_pressed
        r = randint(0, 3)
        if r == 0:
            self._color = (255, 0, 0)
        if r == 1:
            self._color = (255, 255, 255)
        if r == 2:
            self._color = (255, 255, 0)
        if r == 3:
            self._color = (0, 255, 255)

    def get_frame(self):
        """Return an array of integers representing the current state of the animation"""
        leds = [(0, 0, 0)] * 88
        leds[self._key_pressed] = self._color
        self._key_pressed -= 1
        return leds

    def is_complete(self):
        """True if this animation is complete and can be removed"""
        return self._key_pressed < 0

class ChristmasKeyPressAnimation(PressureKeyPressAnimation):
    """Simple animation that happens when you press a key. It is pressure sensitive."""

    def __init__(self, keys, key_pressed, velocity, duration=1000):
        """Initializes a new ChristmasKeyPressAnimation instance"""
        PressureKeyPressAnimation.__init__(self, keys, key_pressed, velocity, duration)
        color = randint(0, 2)

        if color == 0:
            self._color = (velocity, 0, 0)
        if color == 1:
            self._color = (0, velocity, 0)
        if color == 2:
            self._color = (velocity, velocity, velocity)

    def get_key_color(self):
        """Overrides the default and return a Christmasey color"""
        return self._color

class RunningAnimation(Animation):
    """Animation the moves each time a key is pressed"""
    def __init__(self, keys, milliseconds=None):
        Animation.__init__(self, milliseconds)
        # This will hold the active key animations
        self._animations = []
        self._keys = keys
        self._key = 0

    def key_pressed(self, velocity):
        """Call whenever a key is pressed"""
        self._animations.append(PressureKeyPressAnimation(self._keys, self._key, velocity, 1000, self._milliseconds))
        self._key = self._key + 1
        self._key = self._key % self._keys

    def get_frame(self):
        leds = [(0, 0, 0)] * self._keys
        for current_animation in self._animations:
            new_frame = current_animation.get_frame()
            for i, frame_pixel in enumerate(new_frame):
                r, g, b = (frame_pixel)
                if r > 0 or g > 0 or b > 0:
                    leds[i] = frame_pixel

        # Remove keys that are complete
        self._animations = [x for x in self._animations if not x.is_complete()]

        return leds

    def is_complete(self):
        return False
