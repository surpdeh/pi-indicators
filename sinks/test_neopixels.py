import sinks.neopixels

def test_createPixelMap():
    assert sinks.neopixels.createPixelMap("1-2") == [0, 1]
    assert sinks.neopixels.createPixelMap("1 - 2") == [0, 1]
    assert sinks.neopixels.createPixelMap("1-2,4") == [0, 1, 3]
    assert sinks.neopixels.createPixelMap("1-2,4,5-6") == [0, 1, 3, 4, 5]
    assert sinks.neopixels.createPixelMap("1,2-4,6") == [0, 1, 2, 3, 5]
    assert sinks.neopixels.createPixelMap("1,2,3") == [0, 1, 2]
    assert sinks.neopixels.createPixelMap("1,2-3, 4-5") == [0, 1, 2, 3, 4]