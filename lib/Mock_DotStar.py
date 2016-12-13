"""
A drop in replacment for the Adafruit_DotStar module.
It allows me to to visualize what the LED strip may look like, without actually having one.
"""

from graphics import GraphWin, Circle, Point

class Adafruit_DotStar:
    "A mock implementation of the Adafruit_DotStart that simulates LEDs in the UI"
    def __init__(self, nleds, datapin=None, clockpin=None):
        pass
    def begin(self):
        "Mock - Initialize pins/SPI for output. Here it opens a window."
        win = GraphWin("My Circle", 100, 100)
        circle = Circle(Point(50, 50), 10)
        circle.draw(win)
        win.getMouse() # Pause to view result
        win.close()    # Close window when done
