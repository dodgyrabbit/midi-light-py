# midi-light-py
An LED strip controlled by a Raspberry PI and MIDI keyboard.
The side motivation for this was to learn Python, as I've never done any Python projects.

# Overview
Add some lighting effects to your music, by attaching an LED strip and Raspberry PI to your MIDI keyboard.
The MIDI output is used as an input to the RPI and processed to create various effects. Place the
LED strip behind your keyboard for a nice effect.

The project was developed on Linux using [Visual Studio Code](http://code.visualstudio.com/) but pretty sure you can make it work on Windows or Mac.

## Hardware
* [Raspberry Pi 3](https://www.raspberrypi.org/) - Older Pi will also work. I got this one so I can add a [Perma Proto HAT] (https://www.adafruit.com/products/2314)
* [DotStar LED Strip 60 LED] (https://www.adafruit.com/products/2239) - 2M of this will be plently. A full size Piano is about 1.5 M with 88 keys. At 60 LEDs per M this gives you the correct density to have an LED per note on a full size Piano.
* [5V 10A switching power supply](https://www.adafruit.com/products/658) - Probably overkill but I want to be able to drive all LEDs (60mA each) at full strength as a nice backlight.
* [3V-5V Level shifter](https://www.adafruit.com/products/1787) - The RPI GIO pins are 3.3V but the DotStar LED strip expects 5V. Use this level shifter to compensate.
* [USB-MIDI interface] (http://www.ebay.com/itm/New-USB-IN-OUT-MIDI-Interface-Cable-Converter-to-PC-Music-Keyboard-Adapter-Cord-/361501225810) - This cheap interface seems to work just fine.

## Wall mount
* A wood light fixture that houses the RPI and LED lights.
* The fixture appears to "float" mid air with LED strip lighting from the top.
* Power (for RPI and LED strip) and MIDI cables connects to the fixture.

## Software
The software is written in Python. The following libraries are used:
### [mido](https://github.com/olemb/mido)
A Python library that allows you to parse MIDI messages.

`sudo pip install mido`

### libportmidi-dev

`sudo apt-get install libportmidi-dev`

### [graphics.py](http://mcsp.wartburg.edu/zelle/python/graphics.py)

I had to install this dependency to get it to work

`sudo apt-get install python-tk`

### Quick test
To verify if your USB device is working properly, run the following quick Python test

```python
import mido
backend =  mido.Backend()
print backend.get_input_names()
```
If you get something like this
`[u'Midi Through Port-0', u'USB2.0-MIDI MIDI 1']`
you're golden. The **USB2.0-MIDI MIDI 1** is what you want to see.

#Installation

TODO Add proper install instructions here.

This repository uses Git submodules. If the /lib folder is empty, use the commands below to update. Newer versions of Git automatically pulls them during initial clone.

```
git clone https://github.com/dodgyrabbit/midi-light-py
git submodule init
git submodule update
```





