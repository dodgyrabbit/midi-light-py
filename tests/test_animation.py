"""Animation unit tests module"""
import unittest
from  midilightpy import animation

class AnimationTest(unittest.TestCase):
    """Verify all the animations working"""

    def test_keypress_one_key(self):
        """Test that an animation with one key returns a LED that is on"""
        result = animation.LightUpAnimation(1, 0, 0)
        self.assertEqual(result.get_frame(), [(255, 255, 255)])

    def test_keypress_two_keys(self):
        """Test that an animation with two LEDs has one on and one off"""
        result = animation.LightUpAnimation(2, 0, 0)
        self.assertEqual(result.get_frame()[0], (255, 255, 255))
        self.assertEqual(result.get_frame()[1], (0, 0, 0))

    def test_keypress_is_complete(self):
        """Test that an animation with two LEDs has one on and one off"""
        current_milliseconds = 0
        result = animation.LightUpAnimation(1, 0, 1, lambda: current_milliseconds)
        self.assertFalse(result.is_complete(), "Expected that animation is not over yet")
        current_milliseconds = current_milliseconds+1
        self.assertFalse(result.is_complete(), "Expected that animation is over")

    def test_running_key_press(self):
        """Test that pressing a key creates new animations"""
        current_milliseconds = 0
        anim = animation.RunningAnimation(10, lambda: current_milliseconds)
        # No key pressed yet - so no animation on frame 1
        self.assertEqual(anim.get_frame()[0], (0, 0, 0))
        anim.key_pressed(1)
        self.assertNotEqual(anim.get_frame()[0], (0, 0, 0))
        self.assertEqual(anim.get_frame()[1], (0, 0, 0))
        anim.key_pressed(1)
        self.assertNotEqual(anim.get_frame()[0], (0, 0, 0))
        self.assertNotEqual(anim.get_frame()[1], (0, 0, 0))
        self.assertEqual(anim.get_frame()[2], (0, 0, 0))
