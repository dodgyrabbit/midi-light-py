"""
A drop in replacment for the Adafruit_DotStar module.
It allows me to to visualize what the LED strip may look like, without actually having one.
"""

from lib.graphics import GraphWin, Circle, Point, color_rgb

class Adafruit_DotStar:
    "A mock implementation of the Adafruit_DotStart that simulates LEDs in the UI"

    __LED_RADIUS = 5
    __WINDOW_HEIGHT = 300
    __win = None
    __pixels = None
    __numPixels = 0
    __leds = []

    def __init__(self, numPixels):
        print("Inside initializer")
        self.__numPixels = numPixels
        self.__pixels = [0] * numPixels
        print(self.__pixels)

    def getPixel(self, index):
        print("getPixel called in Mock_DotStar")
        return self.__pixels(index)

    def begin(self):
        print( "begin called in Mock_DotStar")
        # Width of window is the number of keys * (diameter + spacing) and then add a diameter on each side for spacing
        self.__win = GraphWin("PianoPy", self. __numPixels * self.__LED_RADIUS * 2 +  self.__numPixels * (self.__LED_RADIUS/2) + 4 * self.__LED_RADIUS, self.__WINDOW_HEIGHT)
        x = 2 * self.__LED_RADIUS
        y = self.__WINDOW_HEIGHT // 2
        for pixel in self.__pixels:
            c = Circle(Point(x, y), self.__LED_RADIUS)

            b = pixel & 255
            g = (pixel >> 8) & 255
            r = (pixel >> 16) & 255
            c.setFill(color_rgb(r, g, b))

            c.draw(self.__win)
            self.__leds.append(c)
            x += self.__LED_RADIUS * 2 + self.__LED_RADIUS / 2

    def setBrightness(self, brightness):
        print("setBrightness called in Mock_DotStar")

    def setPixelColorRGB(self, index, r, g, b):
        self.__pixels[index] = b + g << 8 + r << 16

    def setPixelColor(self, index, color):
        self.__pixels[index] = color

    def clear(self):
        print("Clearing strip data")
        # Set strip data to 'off' (just clears buffer, does not write to strip)
        self.__pixels = [0] * self.__numPixels

    def show(self):
        for led, pixel in zip(self.__leds, self.__pixels):
            b = pixel & 255
            g = (pixel >> 8) & 255
            r = (pixel >> 16) & 255
            led.setFill(color_rgb(r, g, b))
