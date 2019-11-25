# The MIT License (MIT)0
#
# Copyright (c) 2017 Dan Halbert for Adafruit Industries
# Copyright (c) 2017 Kattni Rembor, Tony DiCola for Adafruit Industries
# Copyright (c) 2019 Mason Egger
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
 
import array
import math
from adafruit_circuitplayground.express import cpx
import audiobusio  
import board
import neopixel
import random
import time
 

# Number of samples to read at once.
NUM_SAMPLES = 500
 

 
 
# Remove DC bias before computing RMS.
 
 
def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )
 
    return math.sqrt(samples_sum / len(values))
 
 
def mean(values):
    return sum(values) / len(values)
 

mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                       sample_rate=16000, bit_depth=16)
 
# Record an initial sample to calibrate. Assume it's quiet when we start.
samples = array.array('H', [0] * NUM_SAMPLES)
mic.record(samples, len(samples))
# Set lowest level to expect, plus a little.
 
peak = 0
cpx.pixels.brightness = 0.1
while True:
    if cpx.button_a:
            cpx.pixels.brightness += 0.1
            time.sleep(0.5)
    elif cpx.button_b:
            cpx.pixels.brightness -= 0.1
            time.sleep(0.5)
    else:
        mic.record(samples, len(samples))
        magnitude = normalized_rms(samples)
        if magnitude > 10:
            cpx.pixels.fill((random.randrange(255), random.randrange(255), random.randrange(255)))
        else:
            cpx.pixels.fill(0)
