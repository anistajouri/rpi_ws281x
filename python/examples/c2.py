# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from neopixel import *

import argparse
import signal
import sys

from PIL import Image, ImageDraw, ImageFont

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]


def colourTuple(rgbTuple):
    return Color(rgbTuple[1],rgbTuple[0],rgbTuple[2])

def get_screen():
  screen = [0] * 256
  a = 0
  for x in xrange(0,256,16):
      s = ""
      for i in range(x+0,x+8):
        s += str(i) +","

        screen[a] = i
        a = a + 1
      print(s)


      x = x + 8
      s = ""
      for i in reversed(range(x+0,x+8)):
        s += str(i) +","
        screen[a] = i
        a = a + 1      
      print(s)

  return chunks(screen,8)

def signal_handler(signal, frame):
        colorWipe(strip, Color(0,0,0))
        sys.exit(0)

def opt_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store_true', help='clear the display on exit')
        args = parser.parse_args()
        if args.c:
                signal.signal(signal.SIGINT, signal_handler)

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
#LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering


my_screen = get_screen()

def set_pixel(x, y, color):
    strip.setPixelColor(my_screen[x][y] , color)
    strip.show()

def fill_rectangle(x1, y1, x2, y2, color):
    for x in range(x1, x2):
        for y in range(y1, y2):
          strip.setPixelColor(my_screen[x][y] , color)
    strip.show()

def get_text_size(font,text):
    return font.getsize(text)

def text_to_screen(font, text, cols, lines):
    """Convert text to ASCII art text banner"""
    image = Image.new('RGB', (cols - 1, lines - 1), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, fill='black', font=font)
    width, height = image.size
    pixels = image.load()
#    print("w/h",width,height)
    for y in range(height):
        for x in range(width):
            pix = pixels[x, y]
            if pix != (255, 255, 255):
                print("in:",x,y)
                strip.setPixelColor(my_screen[x][y] , Color(255, 0, 0))
                strip.show()
            else:
                strip.setPixelColor(my_screen[x][y] , Color(0, 0, 255))
                print("ou:",x,y)
                strip.show()

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
#  """Wipe color across display a pixel at a time."""
  #for i in range(strip.numPixels()):
    strip.setPixelColor(248, color)
    strip.show()
    time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
  """Movie theater light style chaser animation."""
  for j in range(iterations):
    for q in range(3):
      for i in range(0, strip.numPixels(), 3):
        strip.setPixelColor(i+q, color)
      strip.show()
      time.sleep(wait_ms/1000.0)
      for i in range(0, strip.numPixels(), 3):
        strip.setPixelColor(i+q, 0)

def wheel(pos):
  """Generate rainbow colors across 0-255 positions."""
  if pos < 85:
    return Color(pos * 3, 255 - pos * 3, 0)
  elif pos < 170:
    pos -= 85
    return Color(255 - pos * 3, 0, pos * 3)
  else:
    pos -= 170
    return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
  """Draw rainbow that fades across all pixels at once."""
  for j in range(256*iterations):
    for i in range(strip.numPixels()):
      strip.setPixelColor(i, wheel((i+j) & 255))
    strip.show()
    time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
  """Draw rainbow that uniformly distributes itself across all pixels."""
  for j in range(256*iterations):
    for i in range(strip.numPixels()):
      strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
    strip.show()
    time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
  """Rainbow movie theater light style chaser animation."""
  for j in range(256):
    for q in range(3):
      for i in range(0, strip.numPixels(), 3):
        strip.setPixelColor(i+q, wheel((i+j) % 255))
      strip.show()
      time.sleep(wait_ms/1000.0)
      for i in range(0, strip.numPixels(), 3):
        strip.setPixelColor(i+q, 0)



MATRIX_WIDTH=32
MATRIX_HEIGHT=8


# Main program logic follows:
if __name__ == '__main__':
  # Process arguments
#  opt_parse()

  text = 'Scrolling ASCII text in console.'

  font = ImageFont.load_default()
  # font = ImageFont.truetype('arial.ttf', 16)

  # get size of space char
  space_width = get_text_size(font, ' ')[0]

  # get size of text
  text_height = get_text_size(font, text)[1]

  # resize console
  cols = 32
  print(text_height)
  lines = int(text_height * 0.75)

  print("---------")
  # Open the image file given as the command line parameter
  try:
    loadIm=Image.open(sys.argv[1])
  except:
    if len(sys.argv)==0:
      raise Exception("Please provide an image filename as a parameter.")
    else:
      raise Exception("Image file %s could not be loaded" % sys.argv[1])

  # If the image height doesn't match the matrix, resize it
  if loadIm.size[1] != MATRIX_HEIGHT:
    origIm=loadIm.resize((loadIm.size[0]/(loadIm.size[1]//MATRIX_HEIGHT),MATRIX_HEIGHT),Image.BICUBIC)
  else:
    origIm=loadIm.copy()
  # If the input is a very small portrait image, then no amount of resizing will save us
  if origIm.size[0] < MATRIX_WIDTH:
    raise Exception("Picture is too narrow. Must be at least %s pixels wide" % MATRIX_WIDTH)        

  # Add a copy of the start of the image, to the end of the image,
  # so that it loops smoothly at the end of the image
  im=Image.new('RGB',(origIm.size[0]+MATRIX_WIDTH,MATRIX_HEIGHT))
  im.paste(origIm,(0,0,origIm.size[0],MATRIX_HEIGHT))
  im.paste(origIm.crop((0,0,MATRIX_WIDTH,MATRIX_HEIGHT)),(origIm.size[0],0,origIm.size[0]+MATRIX_WIDTH,MATRIX_HEIGHT))


#    rg=im.crop((x,0,x+MATRIX_WIDTH,MATRIX_HEIGHT))
  rg=im.crop((0,0,MATRIX_WIDTH,MATRIX_HEIGHT))
  dots=list(im.getdata())
  # print("--------------------------")
  # print(rg)
  print(dots)
  print(my_screen)

  # add some padding to the text
#  padding = ' ' * int(cols / space_width + 1)
#  text = padding + text

  # Create NeoPixel object with appropriate configuration.
  #strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
 
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  # Intialize the library (must be called once before other functions).
  strip.begin()
  print(my_screen[2][1])
#  strip.setPixelColor(255,Color(255,0,0))
  strip.show()
  print ('Press Ctrl-C to quit.')
  while True:
  #  print ('hellworld.')

    colorWipe(strip, Color(255, 0, 0))  # Red wipe
    #colorWipe(strip, 248, Color(255,0,0))
#    for x in range(MATRIX_WIDTH):
#      for y in range(MATRIX_HEIGHT):      
#        for i in range(len(dots)):
#            print(x,y,dots[i])
#            strip.setPixelColor(my_screen[x][y],colourTuple(dots[i]))
  #  strip.show()


#    text_to_screen(font, text, cols, lines)
    # colorWipe(strip, Color(255, 0, 0))  # Red wipe
    # colorWipe(strip, Color(0, 255, 0))  # Blue wipe
    # colorWipe(strip, Color(0, 0, 255))  # Green wipe
    # print ('Theater chase animations.')
    # theaterChase(strip, Color(127, 127, 127))  # White theater chase
    # theaterChase(strip, Color(127,   0,   0))  # Red theater chase
    # theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
    # print ('Rainbow animations.')
    # rainbow(strip)
    # rainbowCycle(strip)
    # theaterChaseRainbow(strip)
