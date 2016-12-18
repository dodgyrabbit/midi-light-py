"""
A drop in replacment for the Adafruit_DotStar module.
It allows me to to visualize what the LED strip may look like, without actually having one.
"""

from lib.graphics import GraphWin, Circle, Point, color_rgb

class Adafruit_DotStar:
    "A mock implementation of the Adafruit_DotStart that simulates LEDs in the UI"

    _LED_RADIUS = 5
    _WINDOW_HEIGHT = 300

    def __init__(self, numPixels):
        print("Inside initializer")
        self._numPixels = numPixels
        self._pixels = [0] * numPixels
        self._win = None
        self._leds = []
        print(self._pixels)

    def getPixel(self, index):
        print("getPixel called in Mock_DotStar")
        return self._pixels(index)

    def begin(self):
        print( "begin called in Mock_DotStar")
        # Width of window is the number of keys * (diameter + spacing) and then add a diameter on each side for spacing
        self._win = GraphWin("PianoPy", self. _numPixels * self._LED_RADIUS * 2 +  self._numPixels * (self._LED_RADIUS/2) + 4 * self._LED_RADIUS, self._WINDOW_HEIGHT)
        x = 2 * self._LED_RADIUS
        y = self._WINDOW_HEIGHT // 2
        for pixel in self._pixels:
            c = Circle(Point(x, y), self._LED_RADIUS)
            r, g, b = _int_to_rgb(pixel)
            c.setFill(color_rgb(r, g, b))
            c.draw(self._win)
            self._leds.append(c)
            x += self._LED_RADIUS * 2 + self._LED_RADIUS / 2

    def setBrightness(self, brightness):
        print("setBrightness called in Mock_DotStar")

    def setPixelColorRGB(self, index, r, g, b):
        # TODO: have one function and parameter count - this way we can have parity with the original library
        self._pixels[index] = _rgb_to_int(r, g, b)

    def setPixelColor(self, index, color):
        self._pixels[index] = color

    def clear(self):
        print("Clearing strip data")
        # Set strip data to 'off' (just clears buffer, does not write to strip)
        # TODO: Optimize - just set the values to 0 so we don't make a list each time. Not sure what the best way in Python is
        self._pixels = [0] * self._numPixels
        
    def _rgb_to_int(r, g, b):
        return  b + (g << 8) + (r << 16)
    
    def _int_to_rgb(color):
        return ((pixel >> 16) & 255, (pixel >> 8) & 255, pixel & 255)

    def show(self):
        for led, pixel in zip(self._leds, self._pixels):
            r, g, b = _int_to_rgb(pixel)
            led.setFill(color_rgb(r, g, b))
