"""
The main beast.
"""

from Mock_DotStar import Adafruit_DotStar
import time

strip = Adafruit_DotStar(88)
strip.begin()
strip.show()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    ## Close mock library (which should close window)
    pass
