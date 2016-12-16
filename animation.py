""" The various classes relating to animations """

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


class KeyPressAnimation(Animation):
    """Simple animation that happens when you press a key"""

    def __init__(self, leds, key_pressed):
        """Initializes a new KeyPressAnimation instance"""
        Animation.__init__(self, leds)
        self.__key_pressed = key_pressed
        self.__leds = leds

    def get_frame(self):
        """Return an array of integers representing the current state of the animation"""
        #self.__leds[self.__key_pressed] = 0xFFFFFF
        leds = [(0, 0, 0)] * 88
        leds[self.__key_pressed] = (255, 255, 255)
        return leds

    def is_complete(self):
        """True if this animation is complete and can be removed"""
        return True
