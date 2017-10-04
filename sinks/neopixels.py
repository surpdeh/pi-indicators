import time
import re
from neopixel import *

def theaterChase(strip, pixelmap, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, len(pixelmap), 3):
                print "q: %s  i: %s  i+q: %s  len(pixelmap): %s" % (q, i, i+q, len(pixelmap))
                strip.setPixelColor(pixelmap[(i+q) %  len(pixelmap)]-1, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, len(pixelmap), 3):
                strip.setPixelColor(pixelmap[(i+q) % len(pixelmap)]-1, 0)

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

def setup(config):
    global __strip__
    sinks = {}
    neoConfig = config['config']


    __strip__ = Adafruit_NeoPixel(\
    #__strip__ = NeoPixel_Stub(\
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

    pattern = "Blink"  # default
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
    theaterChase(__strip__,\
        createPixelMap(config['LEDS']),\
        Color(127, 127, 127))
    print "Finishing pixel animation pattern %s on %s" % (pattern, config['LEDS'])
    return


def createPixelMap(stringMap):
    match = re.match(r"(\d+)-(\d+)", stringMap)
    return range(int(match.group(1)), int(match.group(2))+1)

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

#class Color:
#    def __init__(self, R, G, B):
#        self.R = R
#        self.G = G
#        self.B = B



#__strip__
if __name__ == "__main__":
    import sys
    #  config:
    #    LED_COUNT: 8 # Number of LED pixels.
    #    LED_PIN: 18 # GPIO pin connected to the pixels (must support PWM!).
    #    LED_FREQ_HZ: 800000 # LED signal frequency in hertz (usually 800khz)
    #    LED_DMA: 5 # DMA channel to use for generating signal (try 5)
    #    LED_BRIGHTNESS: 20 # Set to 0 for darkest and 255 for brightest
    #    LED_INVERT: False 

    setup({'config': {'LED_COUNT': 8, 'LED_PIN': 18, 'LED_FREQ_HZ': 800000, 'LED_DMA': 5, 'LED_BRIGHTNESS': 20, 'LED_INVERT': False}, \
           'sink': {} })

    #  GitCommitPixels:
    #      LEDS: 1-2
    #      regex: Ping (\d+)
    #      PatternMap:
    #        '1': Blink
    #        '2': Chaser
    match = re.match("Ping (\d+)", "Ping 2")
    playPixels({'LEDS': '3-10', 'regex': 'Ping (\d+)', 'PatternMap': { '1': 'Blink', '2': 'Chaser'}}, match)
