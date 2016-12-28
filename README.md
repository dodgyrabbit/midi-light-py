# midi-light-py
A wall mounted ambient light panel that responds to your MIDI based keyboard. It is a Raspberry PI based projected written in Python.

# Overview
Add some visual effects to your tunes by attaching an LED strip and Raspberry PI to your MIDI keyboard. The MIDI output is used as an input 
to the RPI and processed in real-time to create various mood effects. In this project I created a "floating" wooden panel to hide the LED
strip and blend in with the environment. The LEDs also project onto the wall for greater visual effect.

# Installation

Clone the repo locally on your Raspberry PI. This repository uses Git submodules.
If the /lib folder is empty, use the commands below to update. Newer versions of Git automatically pulls them during initial clone.

```
git clone https://github.com/dodgyrabbit/midi-light-py.git
git submodule init
git submodule update
```

Ensure all the dependencies (noted below) are installed run

```
pip install -r requirements.txt
```

To start:
```
python main.py
```

## Hardware
* [Raspberry Pi](https://www.raspberrypi.org/) - I'm using on of the originals but newer PIs will work too. 
* [DotStar LED Strip 60 LED] (https://www.adafruit.com/products/2239) - A full size Piano is about 1.5 M with 88 keys. At 60 LEDs per M this gives you about the correct density to have an LED per note on a full size Piano. I used the remaining LEDs to light up the bottom part of the light fixture.
* [5V 10A switching power supply](https://www.adafruit.com/products/658) - Probably overkill but I want to be able to drive all LEDs (60mA each) at full strength as a nice backlight.
* [USB-MIDI interface] (http://www.ebay.com/itm/New-USB-IN-OUT-MIDI-Interface-Cable-Converter-to-PC-Music-Keyboard-Adapter-Cord-/361501225810) - This cheap interface seems to work just fine.

Note that AdaFruit recommends a [level shifter](https://www.adafruit.com/products/1787) be used since the RPI GIO pins are 3.3V but the DotStar LED strip expects 5V. However, I found that with this level shifter the
first LED on my strip would misbehave and I got strange results. It turns out that the DotStar worked perfectly fine without it.

## Wall mount
* A wooden light fixture that houses the RPI and LED lights and attaches to the wall.
* The fixture appears to float on the wall and the LED strip is at the top (the part that responds to notes) and a bottom light for status or reading your music.

## Software
* The project was mostly developed on Linux using [Visual Studio Code](http://code.visualstudio.com/).
* On the RPI itself I used nano.
* The software is written in Python.

### [mido](https://github.com/olemb/mido)
A Python library that allows you to parse MIDI messages.

### [rtmidi-python](https://github.com/superquadratic/rtmidi-python)

### [graphics.py](http://mcsp.wartburg.edu/zelle/python/graphics.py)
Graphics.py is used to simulate the LED strip. This saves a bit of time because developing directly on the RPI is a little more challenging (although I did a lot of that).

Note: On Linux I had to install this dependency to get it to work

`sudo apt-get install python-tk`

### Quick test
To verify if your USB device is working properly, run the following quick Python test

```python
import mido
backend = mido.Backend('mido.backends.rtmidi')
print backend.get_input_names()
```
If you get something like this
`[u'Midi Through Port-0', u'USB2.0-MIDI MIDI 1']`
you're golden. The **USB2.0-MIDI MIDI 1** is what you want to see (on a Linux Desktop.)
On the RPI the string was similar to "MIDI 1".






