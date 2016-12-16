# Thoughts

I did a bit of Googling around and found [BiblioPixel](https://github.com/ManiacalLabs/BiblioPixel). It has some interesting parts to me. It has a basic
framework for doing animations.

However, the main idea here is that animations repeat. You could queue animations, but still, it's essentially just a series of animations, which itself can be looped.

## What do I need?
* Animations are based on inputs. When a key is pressed, it triggers a visualization of that note (or perhaps of a chord, beat or something else). Other inputs may
include a key being released, the duration a key is held (or not) and the velocity of the key.
* There can be multiple animations going on at any time. For example, you are pressing 3 notes - three different parts of the LED strip can light up.
* Animations may "linger" after an input has gone.
* Animations may affect neighboring pixels.
* Animations need to be able to be "blended" or "overlayed". For example, if pressing a note makes the main LED light up, there may be surrounding ones that light up too.
* How these "overlays" or "blending" works need to be defined.

## Ideas for animations
1. Simplest one - simply turn an LED on for the equivalent note that is pressed. Turn it off when the note is released.
2. Like [1] but instead "fade out" as you release the LED.
3. Like [2] but "fade in" and "fade out".
4. Variations above where brightness is proportional to the velocity of the key.
5. Chord detection - change color for certain chords - like minor chords turn blue, major chords white, diminished chords turn red etc.
6. Beat detection - pulse the lights.
7. Beat indicator - use a few, or all, of the leds to set the tempo, while doing animations.

## Problems to solve in code
* How to make composable animations. I.e. a system of "layering" or combining them.
* How to blend them.
* Creating a class that encapsulates a particular animations.
    * Do we define certain "steps" in the animation?
    * How do these steps related to FPS? Does one step simply refer to a "frame".
    * Given an animation "state" - should you be able to move forward/backwards through frames.
    * Can an animation be mutated. I.e. once you define the animation, can it be changed or is each frame simply a function of which step it's in? If you want a different 
      behaviour then create a new animation object?
    * Assuming state can mutate - is there a point where it's "done"?

Each animation is essentially a small state machine, that "steps" each time a frame is needed.

Question - does the animation care "where" it is? Should animation perhaps be given an anchor point - but it then defines how surrounding pixels are affected. This way you 
could simply apply the "fade on" animation to pixel 34 and it would automatically be applied. 

Maybe the animation should be "done" when it no longer affects any pixels (all values are back to 0).

This would mean animations could linger on for quite some time - for example, I press Middle C - then it lights up a number of pixels. I release it, they start fading away. 
Then I press it again. It would then light up the surrounding pixels "more" because of the first animation that is still fading away. If I did this repeatedly, you could 
effectively light up a whole bunch of pixels.

Random idea - "bleeding" of light means if I'm at 80% my neighbors are at 40%, their neighbors at 20% etc. If I did this,  it would mean you could in theory keep lighting 
up more and more pixels by repeatedly hitting one note.
