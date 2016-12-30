""" The various classes relating to animations """
from __future__ import print_function
from __future__ import division

from random import randint
import time

class Animation(object):
    """The base class for any animation"""
    def __init__(self, milliseconds=None):
        """ Animation base class initializer """
        object.__init__(self)
        if milliseconds is None:
            self._milliseconds = lambda: int(round(time.time() * 1000))
        else:
            self._milliseconds = milliseconds

    def get_frame(self):
        """Return an array of integers representing the current state of the animation"""
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

class KeyPressAnimation(Animation):
    """Simple animation that happens when you press a key"""

    def __init__(self, keys, key_pressed, duration=1000, milliseconds=None):
        """Initializes a new KeyPressAnimation instance"""
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

class PressureKeyPressAnimation(KeyPressAnimation):
    """Simple animation that happens when you press a key. It is pressure sensitive."""

    def __init__(self, keys, key_pressed, velocity, duration=1000):
        """Initializes a new PressureKeyPressAnimation instance"""
        KeyPressAnimation.__init__(self, keys, key_pressed, duration)
        self._velocity = velocity
        self._duration = duration

    def get_key_color(self):
        """Returns the color of the key pressed during animation. Override to change. """
        return (self._velocity, self._velocity, self._velocity)

    def get_frame(self):
        """Return an array of integers representing the current state of the animation"""

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
