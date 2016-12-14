"""
A drop in replacment for the Adafruit_DotStar module.
It allows me to to visualize what the LED strip may look like, without actually having one.
"""

from graphics import GraphWin, Circle, Point, color_rgb

class Adafruit_DotStar:
    "A mock implementation of the Adafruit_DotStart that simulates LEDs in the UI"

    __LED_RADIUS = 5
    __WINDOW_HEIGHT = 300
    __win = None
    __pixels = None
    __numPixels = 0

    def __init__(self, numPixels):
        print "Inside initializer"
        self.__numPixels = numPixels
        self.__pixels = range(0, numPixels)
        print self.__pixels

    def getPixel(self, index):
        print "getPixel called in Mock_DotStar"
        return self.__pixels(index)

    def begin(self):
        print "begin called in Mock_DotStar"
        # Width of window is the number of keys * (diameter + spacing) and then add a diameter on each side for spacing
        self.__win = GraphWin("PianoPy", self. __numPixels * self.__LED_RADIUS * 2 +  self.__numPixels * (self.__LED_RADIUS/2) + 4 * self.__LED_RADIUS, self.__WINDOW_HEIGHT)

    def setBrightness(self, brightness):
        print "setBrightness called in Mock_DotStar"

    def setPixelColor(self, index, r, g, b):
        self.__pixels[index] = b + g << 8 + r << 16

    def clear(self):
        print "Clearing strip data"
        # Set strip data to 'off' (just clears buffer, does not write to strip)
        # There's probably a better way of doing this... this creates a new list I think
        self.__pixels = range(0, self.__numPixels, 0)

    def show(self):
        x = 2 * self.__LED_RADIUS
        y = self.__WINDOW_HEIGHT // 2
        for pixel in self.__pixels:
            c = Circle(Point(x, y), self.__LED_RADIUS)

            b = pixel & 255
            g = (pixel >> 8) & 255
            r = (pixel >> 16) & 255
            c.setFill(color_rgb(r, g, b))

            c.draw(self.__win)
            x += self.__LED_RADIUS * 2 + self.__LED_RADIUS / 2
