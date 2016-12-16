# Main Loop

The main loop has a number of stages:
* Apply an optional filter (default is to black out LEDs).
* Process all animations and write them into LED buffer. 
* Destroy animations that are complete.
* Update the LED display.
* Process any inputs and create any new animations as needed.
* Sleep to achieve the desired frame rate.

## Classes

### Animator
This is the main loop - I guess it does not need to be a class all by itself but lets go with it for now.
* Encapsulates the main loop and takes an LED strip as parameter
* Has a Run method that runs continuously
* Provides a way to "end" the loop

### Animation
* Base class for any animation
* An animation is a class that produces a series of "frames" for a given state
* The state of an animation may be altered
* An animation "key" must be defined so we can find it again later if the animation state changes

### AnimationCoordinator


### Filter 
* Takes the current state of the LED "buffer" and applies some kind of filter to it.
* The most basic filter is to set it back to all zero's between frames.
* Examples my include "fade out", "fade left", "fire" etc.
* It outputs an new LED buffer.

### LED buffer
* Represents the RGB state for each pixel in the strip 
