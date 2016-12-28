"""
A drop in replacment for the Adafruit_DotStar module.
It allows me to to visualize what the LED strip may look like, without actually having one.
"""

#from lib.graphics import GraphWin, Circle, Point, color_rgb, Rectangle, Text
import graphics

class Adafruit_DotStar:
    "A mock implementation of the Adafruit_DotStart that simulates LEDs in the UI"

    _LED_SIZE = 30
    _WINDOW_HEIGHT = 300
    _WINDOW_WIDTH = 800

    def __init__(self, numPixels, a=None, order=None):
        print("Inside initializer")
        self._numPixels = numPixels
        self._pixels = [0] * numPixels
        self._win = None
        self._leds = []
        print(self._pixels)

    def getPixel(self, index):
        """Returns the color value of the given pixel."""
        return self._pixels(index)

    def begin(self):
        """Opens the Mock_DotStar window."""
        print( "Starting Mock_DotStar")

        self._win = graphics.GraphWin("PianoPy", self._WINDOW_WIDTH, self._WINDOW_HEIGHT)
        self._win.setBackground("black")
        leds_per_row = self._WINDOW_WIDTH // (self._LED_SIZE)
        x = 0
        y = 0

        for i, pixel in enumerate(self._pixels):

            x = (i % leds_per_row) * self._LED_SIZE
            y = (i // leds_per_row) * self._LED_SIZE

            block = graphics.Rectangle(graphics.Point(x, y), graphics.Point(x + self._LED_SIZE - 1, y + self._LED_SIZE - 1))

            r, g, b = ((pixel >> 16) & 255, (pixel >> 8) & 255, pixel & 255)
            block.setFill(graphics.color_rgb(r, g, b))
            block.draw(self._win)

            t = graphics.Text(graphics.Point(x + self._LED_SIZE // 2, y + self._LED_SIZE // 2), str(i))
            t.setSize(10)
            t.setTextColor("white")
            t.draw(self._win)
            self._leds.append(block)

    def setBrightness(self, brightness):
        """Sets the brightness for the whole strip. Not implemented."""
        print("setBrightness called in Mock_DotStar. Not implemented.")

    def setPixelColor(self, index, color_or_r, g = None, b = None):
        """Sets the given LED color value. To be compatible with DotStart library, you can either pass just the color value or r,g,b values."""
        if g is None:
            self._pixels[index] = color_or_r
        else:
            self._pixels[index] = b + (g << 8) + (color_or_r << 16)

    def clear(self):
        """Reset all LED values to 0 (black/off)."""
        print("Clearing strip data")
        # Set strip data to 'off' (just clears buffer, does not write to strip)
        self._pixels = [0] * self._numPixels

    def show(self):
        """Renders the current state of the LEDs to screen."""
        for led, pixel in zip(self._leds, self._pixels):
            r, g, b = ((pixel >> 16) & 255, (pixel >> 8) & 255, pixel & 255)
            led.setFill(graphics.color_rgb(r, g, b))
