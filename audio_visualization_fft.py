#!/usr/bin/env python
''' audio_visualization_fft.py V1.
A Realtime Audio Visualization in python using
a Raspberrypi + Sense HAT and a USB microphone.
Applying Fast Fourier transformation to separate all chanels.

Run the script as root user.
Press Control + C to exit.'''

from sense_hat import SenseHat
import alsaaudio
from time import sleep
from colour import Color
import numpy
import argparse


def show_cards(card=None):
  available_cards = alsaaudio.cards()
  print 'Available sound cards:'
  print '  [%s]' % ', '.join(available_cards)
  print ''
  if card:
   if card not in available_cards:
     available_cards = []
  return available_cards


def hex_to_rgb(colors_list):
  """Return (red, green, blue) for the color given as #rrggbb list."""
  rgb_colors_list = []
  for colors in colors_list:
    value = str(colors.hex_l)
    value = value.lstrip('#')
    lv = len(value)
    rgb_colors_list.append(tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)))
  return rgb_colors_list


def calculate_levels(data):
  """Return [matix] for data given"""

  # Convert to int16
  data = numpy.fromstring(data, dtype='int16')

  # Apply FFT, https://en.wikipedia.org/wiki/Fast_Fourier_transform
  fourier = numpy.fft.rfft(data)

  # Remove last element, same size as chunk
  fourier = numpy.delete(fourier, len(fourier) - 1)

  # Calculate power spectrum, in base 10
  power = numpy.log10(numpy.abs(fourier))**2

  # Generate data with len multiple of 8, solve problems with chunk and setperiodsize
  # print (len(power))
  # power = power[:int(len(power)/8)*8]

  # 8 Rows with power data
  power = numpy.reshape(power, (8, len(power) / 8))

  # Generate average on each row
  matrix = numpy.int_(numpy.average(power, axis= 1)/ 4)

  return matrix


if __name__ == "__main__":

  parser = argparse.ArgumentParser(description='Audio Visualization')
  parser.add_argument('--card',
    help='Select a system sound card.')
  parser.add_argument('--show-cards', action='store_true',
    help='Show all system sound cards.')

  args = parser.parse_args()

  if args.show_cards:
    show_cards()
    quit(1)

  if args.card:
    if not show_cards(args.card):
      print 'Error: card "%s" is not available, choose a valid one.' % args.card
      quit(2)
  else:
    cards = show_cards()
    if cards:
      args.card = cards[0]
    else:
      print 'Error: no sound cards found.'
      quit(2)

  print 'Info: sound card "%s" selected.' % args.card

  # Sound card (check with alsaaudio.cards())
  card         = 'sysdefault:CARD=%s' % args.card

  max_audioop  = 32754             # Max value

  black        = (0, 0, 0)         # Empty
  ini_colors   = ['red','orange','yellow','cyan','blue','magenta','violet','green']
  gradients    = []
  granularity  = 8                 # Granularity level
  for item in ini_colors:
    color = Color(item, luminance=0.15)
    gradients.append(hex_to_rgb(list(color.range_to(Color(item),granularity))))

  #sample_rate = 8000, #In my case setperiodsize not work, change to generate data multiple of 8
  sample_rate = 8282

  channels    = 1
  chunk       = 1024    # Use a multiple of 8

  # Initialize SenseHat
  sense = SenseHat()

  # Initialize Alsa Audio
  inp = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE, mode=alsaaudio.PCM_NORMAL, device=card)
  inp.setchannels(channels)
  inp.setrate(sample_rate)
  inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
  inp.setperiodsize(chunk)

  # Clean screen
  screen = [black] * ( 8 * 8 ) 
  sense.set_pixels(screen)

  # Read From microphone
  try:
    while True:
      l,data = inp.read()
      if l > 1:
        matrix = calculate_levels(data)

        screen = [black] * ( 8 * 8 )

        for x in range(0,8):
          for y in range(0,matrix[x]):
            screen[(y*8)+x] = gradients[x][y] 
        
        sense.set_pixels(screen)
      sleep(.001)

  except (KeyboardInterrupt, SystemExit):

    # Clean screen
    screen  = [black] *( 8 * 8 )
    sense.set_pixels(screen)
