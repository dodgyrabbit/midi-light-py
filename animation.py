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

class FireAnimation(Animation):
    def __init__(self):
        """ Fire animation """
        self._lights = []
    	self._r = 255
        self._g = 255 - 40
        self._b = 40
        self._end = 0

    def get_frame(self):
        if (milliseconds() > self._end):
            self._end = milliseconds() + 50
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

class ChristmasKeyPressAnimation(Animation):
    """Simple animation that happens when you press a key. It is pressure sensitive."""

    def __init__(self, leds, key_pressed, velocity):
        """Initializes a new ChristmasKeyPressAnimation instance"""
        Animation.__init__(self, leds)
        self.__key_pressed = key_pressed
        self.__leds = leds
        self._count = 0
        self._velocity = velocity
        self._end = milliseconds() + 1000
        self._color = randint(0, 2)

    def get_frame(self):
        """Return an array of integers representing the current state of the animation"""
        leds = [(0, 0, 0)] * 88

        if self._color == 0: 
            leds[self.__key_pressed] = (self._velocity, 0, 0)
        if self._color == 1:
            leds[self.__key_pressed] = (0, self._velocity, 0)
        if self._color == 2:
            leds[self.__key_pressed] = (self._velocity, self._velocity, self._velocity)

        self._count += 1
        if self._count % 3 == 0:
            self._velocity = int(self._velocity * 0.9)
        return leds

    def is_complete(self):
        """True if this animation is complete and can be removed"""
        return milliseconds() > self._end




class PressureKeyPressAnimation(Animation):
    """Simple animation that happens when you press a key. It is pressure sensitive."""

    def __init__(self, leds, key_pressed, velocity):
        """Initializes a new PressureKeyPressAnimation instance"""
        Animation.__init__(self, leds)
        self.__key_pressed = key_pressed
        self.__leds = leds
        self._count = 0
        self._velocity = velocity
        self._end = milliseconds() + 1000

    def get_frame(self):
        """Return an array of integers representing the current state of the animation"""
        leds = [(0, 0, 0)] * 88
        leds[self.__key_pressed] = (self._velocity, self._velocity, self._velocity)
        self._count += 1
        if self._count % 3 == 0:
            self._velocity = int(self._velocity * 0.7)
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
