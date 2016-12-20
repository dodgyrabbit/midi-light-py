""" The various classes relating to animations """

from random import randint
import time

milliseconds = lambda: int(round(time.time() * 1000))

class Animation:
    """The base class for any animation"""
    def __init__(self, leds):
        """ Animation base class initializer """

    def get_frame(self):
        """Return an array of integers representing the current state of the animation"""
        raise RuntimeError("GetFrame should only be called in derived classes")

    def is_complete(self):
        """True if this animation is complete and can be removed"""
        return False

class PressureKeyPressAnimation(Animation):
    """Simple animation that happens when you press a key. It is pressure sensitive."""

    def __init__(self, leds, key_pressed, velocity):
        """Initializes a new PressureKeyPressAnimation instance"""
        Animation.__init__(self, leds)
        self.__key_pressed = key_pressed
        self.__leds = leds
        self._count = 0
        self._velocity = velocity
        self._end = milliseconds() + 3000

    def get_frame(self):
        """Return an array of integers representing the current state of the animation"""
        leds = [(0, 0, 0)] * 88
        leds[self.__key_pressed] = (self._velocity, self._velocity, self._velocity)
        self._count += 1
        if self._count % 3 == 0:
            self._velocity = int(self._velocity * 0.9)
        return leds

    def is_complete(self):
        """True if this animation is complete and can be removed"""
        return milliseconds() > self._end

class KeyPressAnimation(Animation):
    """Simple animation that happens when you press a key"""

    def __init__(self, leds, key_pressed):
        """Initializes a new KeyPressAnimation instance"""
        Animation.__init__(self, leds)
        self.__key_pressed = key_pressed
        self.__leds = leds
        self._count = 60

    def get_frame(self):
        """Return an array of integers representing the current state of the animation"""
        leds = [(0, 0, 0)] * 88
        leds[self.__key_pressed] = (255, 255, 255)
        self._count -= 1
        return leds

    def is_complete(self):
        """True if this animation is complete and can be removed"""
        return self._count < 0

class RunLeftAnimation(Animation):
    """Simple animation that happens when you press a key"""

    def __init__(self, leds, key_pressed):
        """Initializes a new KeyPressAnimation instance"""
        Animation.__init__(self, leds)
        self.__key_pressed = key_pressed
        self.__leds = leds
        r = randint(0, 3)
        if r == 0:
            self.__color = (255, 0, 0)
        if r == 1:
            self.__color = (255, 255, 255)
        if r == 2:
            self.__color = (255, 255, 0)
        if r == 3:
            self.__color = (0, 255, 255)

    def get_frame(self):
        """Return an array of integers representing the current state of the animation"""
        leds = [(0, 0, 0)] * 88
        leds[self.__key_pressed] = self.__color
        self.__key_pressed -= 1
        return leds

    def is_complete(self):
        """True if this animation is complete and can be removed"""
        return self.__key_pressed < 0
