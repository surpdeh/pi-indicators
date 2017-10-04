import time
import re

def blink(strip, pixelmap, wait_ms=500, iterations=10):
    """Simple 5 seconds of blinking 50% duty cycle"""
    color = Color(127, 127, 127)
    for j in range(iterations):
        for c in (0, 1):
            for i in range(0, len(pixelmap)):
                strip.setPixelColor(pixelmap[i], color if c==0 else 0) 
            strip.show()
            time.sleep(wait_ms/1000.0)


def theaterChase(strip, pixelmap, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    color = Color(127, 127, 127)
    for j in range(iterations):
        for q in range(3):
            for i in range(0, len(pixelmap), 3):
                strip.setPixelColor(pixelmap[(i+q) %  len(pixelmap)], color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, len(pixelmap), 3):
                strip.setPixelColor(pixelmap[(i+q) % len(pixelmap)], 0)
    strip.show()

def colorWipe(strip, pixelmap, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    color = Color(127, 127, 127)
    for i in range(len(pixelmap)):
        strip.setPixelColor(pixelmap[i], color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def wheel(pos):
    """"Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, pixelmap, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(len(pixelmap)):
            strip.setPixelColor(pixelmap[i], wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, pixelmap, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(len(pixelmap)):
            strip.setPixelColor(pixelmap[i], wheel((int(i * 256 / len(pixelmap)) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, pixelmap, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, len(pixelmap), 3):
                strip.setPixelColor(pixelmap[(i+q) % len(pixelmap)], wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, len(pixelmap), 3):
                strip.setPixelColor(pixelmap[(i+q) % len(pixelmap)], 0)


# Create NeoPixel object with appropriate configuration.
    # shield:
    #   type: neopixel
    #   config:
    #     LED_COUNT: 8 # Number of LED pixels.
    #     LED_PIN: 18 # GPIO pin connected to the pixels (must support PWM!).
    #     LED_FREQ_HZ: 800000 # LED signal frequency in hertz (usually 800khz)
    #     LED_DMA: 5 # DMA channel to use for generating signal (try 5)
    #     LED_BRIGHTNESS: 20 # Set to 0 for darkest and 255 for brightest
    #     LED_INVERT: False 
    #   sink:
    #     GitCommitPixels:
    #       LEDS: 1-2
    #       Pattern: $event

def setup(config, stub=False):
    global __strip__
    sinks = {}
    neoConfig = config['config']


    if stub:
        provider = NeoPixel_Stub
        print "Using neopixel stub only"
    else:
        from neopixel import *
        provider = Adafruit_NeoPixel
        print "Using actual neopixel"

    __strip__ = provider(\
        neoConfig['LED_COUNT'],\
        neoConfig['LED_PIN'],\
        neoConfig['LED_FREQ_HZ'],\
        neoConfig['LED_DMA'],\
        neoConfig['LED_INVERT'],\
        neoConfig['LED_BRIGHTNESS'])

    # Intialize the library (must be called once before other functions).
    __strip__.begin()

    for sinkLabel, sinkSetup in config['sink'].items():
        sinks[sinkLabel] = sinkSetup
        print "Setting up %s" % sinkLabel

    return sinks


def playPixels(config, match):
    global __strip__
    global __patterns__

    pattern = "blink"  # default
    if config.get('PatternMap'):
        if config['PatternMap'].get(match.group(1)):
            pattern = config['PatternMap'][match.group(1)]
        else:
            print "Error in resolving pattern; no mapping for %s in %s" % (match.group(1), config['PatternMap'])

    else:
        if config.get('Pattern'):
            pattern = config['Pattern']
        else:
            print "Error - no PatternMap or Pattern given"

    print "Starting pixel animation pattern %s on %s" % (pattern, config['LEDS'])
    if __patterns__.get(pattern):
        patternFunc = __patterns__[pattern]
    else:
        patternFunc = blink
        print "Error: no known pattern %s" % pattern

    patternFunc(__strip__,\
        createPixelMap(config['LEDS']))

    print "Finishing pixel animation pattern %s on %s" % (pattern, config['LEDS'])
    return


def createPixelMap(stringMap):
    """ Translate a one based string description of addressed pixels into a zero based list """
    match = re.match(r"(\d+)-(\d+)", stringMap)
    return range(int(match.group(1))-1, int(match.group(2)))

class NeoPixel_Stub:
    def __init__(self, LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT):
        print "Init: LED_COUNT: %s   LED_PIN: %s   LED_FREQ_HZ: %s  LED_DMA: %s  LED_BRIGHTNESS: %s  LED_INVERT: %s" % \
            (LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT)

    def begin(self):
        return

    def show(self):
        return

    def setPixelColor(self, pixel, color):
        print "Setting pixel %s color %s" % (pixel, color)
        return

# Reproduce the neopixels utlity function
def Color(red, green, blue, white = 0):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return (white << 24) | (red << 16)| (green << 8) | blue



__patterns__ = {\
   'blink': blink,\
   'theaterChase': theaterChase,\
   'colorWipe': colorWipe,\
   'colourWipe': colorWipe,\
   'rainbow': rainbow,\
   'rainbowCycle': rainbowCycle,\
   'theaterChaseRainbow': theaterChaseRainbow\
}


if __name__ == "__main__":
    import sys
    #  config:
    #    LED_COUNT: 8 # Number of LED pixels.
    #    LED_PIN: 18 # GPIO pin connected to the pixels (must support PWM!).
    #    LED_FREQ_HZ: 800000 # LED signal frequency in hertz (usually 800khz)
    #    LED_DMA: 5 # DMA channel to use for generating signal (try 5)
    #    LED_BRIGHTNESS: 20 # Set to 0 for darkest and 255 for brightest
    #    LED_INVERT: False 

    stubbing = False
    if sys.argv[1] == "stub":
        stubbing = True

    setup({'config': {'LED_COUNT': 32, 'LED_PIN': 18, 'LED_FREQ_HZ': 800000, 'LED_DMA': 5, 'LED_BRIGHTNESS': 10, 'LED_INVERT': False}, \
           'sink': {} },
           stub=stubbing)

    #  GitCommitPixels:
    #      LEDS: 1-2
    #      regex: Ping (\d+)
    #      PatternMap:
    #        '1': Blink
    #        '2': Chaser
    match = re.match("Play (\d+)", sys.argv[2])
    playPixels({'LEDS': '1-32', 'regex': 'Play (\d+)',\
                'PatternMap': { '1': 'blink', '2': 'theaterChase', '3': 'colorWipe', '4': 'rainbow', '5': 'rainbowCycle', '6': 'theaterChaseRainbow' }},\
                 match,
                 )
