Realtime Audio Visualization and Fast Fourier transform
=============

Description
-------
A Realtime Audio Visualization in Python using a Raspberrypi a Sense HAT and a USB microphone.
On this script i use a USB microphone to get the audio, then calculate Fast Fourier transform to represent in the 8 x 8 RGB LED matrix, 

The [Sense Hat](https://www.raspberrypi.org/documentation/hardware/sense-hat/) is an add-on board for [Raspberry Pi](https://www.raspberrypi.org/), made especially for the Astro Pi mission.
The Sense HAT has an 8×8 RGB LED matrix, a five-button joystick and includes the following sensors:
- Gyroscope
- Accelerometer
- Magnetometer
- Temperature
- Barometric pressure
- Humidity

Instalation
-------
```
git clone https://github.com/rfiestas/audio_visualization_fft.git
```
also:

- [sense-hat](https://www.raspberrypi.org/documentation/hardware/sense-hat/), python module to control the Raspberry Pi Sense HAT.
- [alsa audio](https://larsimmisch.github.io/pyalsaaudio), provides audio and MIDI functionality to the Linux operating system.  
- [colour](https://pypi.python.org/pypi/colour), converts and manipulates various color representation (HSL, RVB, web, X11, ...).
- [numphy](http://www.numpy.org/), is the fundamental package for scientific computing with Python.

Usage
-------
Launch this script with any root rights user, Press Contol + C, to stop script.
```
audio_visualization_ttf.py
```

Show sound cards.
```
# ./audio_visualization_fft.py --show-cards
```

Select sound card.
```
# ./audio_visualization_fft.py --card Device
```

Notes:
-------
  - Alsa Audio need libasound2-dev

Troubleshooting:
-------

I can't change setperiodsize, It's automatically calculated, based on rate and numbers of chanels.
it's neccessary get a data lenght multiple of 8, to represent in the screen.
