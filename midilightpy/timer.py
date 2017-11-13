from animation import Animation

class Timer(Animation):
    """A timer implementation that tracks minutes up to an hour"""
    def __init__(self):
        Animation.__init__(self)
        self._start = self._milliseconds() - (9 * 60 * 1000)

    def get_frame(self):
        """Returns 60 tuples indicating the RGB value for the timer"""
        now = self._milliseconds()
        current_milliseconds = (now - self._start) % (60 * 60 * 1000)
        current_seconds = current_milliseconds / 1000
        current_minutes = current_seconds / 60
        current_ten_minute_interval = current_minutes / 10

        pixels = [(0, 0, 0)] * 60

        # Indicate current minute within the 10 minute bracket.
        # If it falls on the 10 minute interval, the next one will overwrite it (10 minute markers take priority)
        pixels[current_minutes] = (128, 128, 128)

        # Light up all the 10 minute markers that has passed. Easy to see how far you are.
        # The first one is skipped (count the number of reds to see how many 10 minutes you're in).
        # To achieve this, add 10. Once 10 minutes have passed the first item in the range is returned.
        for i in range(current_ten_minute_interval):
            pixels[i * 10 + 10] = (255, 0, 0)

        # Indicate current second position.
        pixels[current_seconds % 60] = (0, 255, 0)

        return pixels

    def is_complete(self):
        return False

    def restart(self):
        """Restart the timer."""
        self._start = self._milliseconds()