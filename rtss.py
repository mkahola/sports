#!/usr/bin/env python2

"""
Copyright (c) 2018

Redistribution and use in source and binary forms, with or without
odification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * The names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Author: Mika Kahola <mika.kahola@kolumbus.fi>
"""

import sys
import argparse
import math
import numpy
import datetime

# requires python-fitparse library from
# https://github.com/dtcooper/python-fitparse
from fitparse import FitFile, FitParseError
from scipy.signal import lfilter

class User():
    def __init__(self, ftp, threshold):
        self.ftp = ftp
        self.hr_ftp = threshold

def average (data):
    try:
        avg = sum(filter(None, data))/float(len(filter(None, data)))
    except ZeroDivisionError:
        print("divide by zero")
        return 0

    return avg

def get_hrTSS(hr, duration, threshold):

    if not hr:
        return 0, 0, 0, 0

    hr_avg = sum(hr)/float(len(hr))
    hr_min = min(hr)
    hr_max = max(hr)
    tss = (duration * hr_avg)/(threshold * 3600.0) * 100.0

    return tss, hr_avg, hr_max, hr_min

def get_TSS(speed, vertical_speed, duration, ftp):
    if not speed:
        return 0, 0, 0

    # convert to m/s
    ftp_speed = (60/ftp)/3.6

    ngp = []
    for i in range(1, duration):
        slope = 6 * vertical_speed[i] / speed[i];
        if slope > 0:
            ngp.append(speed[i] / math.cos(math.atan2(slope, 1)))
        else:
            ngp.append(speed[i] * math.cos(math.atan2(slope, 1)))

     # 30s moving average filter
    h = numpy.empty(30)
    h.fill(1.0/30)

    # power of 4 of 30s average power
    p_30s = lfilter(h, 1.0, ngp)**4

    # average of power of 4
    p_avg = average(p_30s)

    # normalized power
    NP = math.sqrt(math.sqrt(p_avg))
    
    IFactor = NP/ftp_speed;

    # training stress score as in trainingpeaks.com
    tss = (duration * NP * IFactor) / (ftp_speed * 3600) * 100.0

    return tss, NP, IFactor

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fitfile", type=str, default="", help="FIT file")
    parser.add_argument("-p", "--ftp",   type=float, default=4.5, help="Functional Threshold Pace")
    parser.add_argument("-t", "--threshold", type=int, default=155, help="Heartrate threshold")
    args = parser.parse_args()

    user = User(args.ftp, args.threshold)

    try:
        fitfile = FitFile(args.fitfile)
        fitfile.parse()
    except FitParseError, e:
        print "Error while parsing .FIT file: %s" % e
        sys.exit(1)
    
    speed = []
    vertical_speed = []
    heartrate = []
    cadence = []
    start = ""
    stop = ""
    distance = 0

    # Get all data messages that are of type record
    for record in fitfile.get_messages('record'):
        
        # Go through all the data entries in this record
        for data in record:
            if data.name == "timestamp":
                if not start:
                    start = data.value
                else:
                    stop = data.value

            if data.name == "speed":
                speed.append(data.value)
            if data.name == "vertical_speed":
                vertical_speed.append(data.value)
            if data.name == "heart_rate":
                heartrate.append(data.value)
            if data.name == "distance":
                if data.value != None:
                    distance = data.value

    duration  = stop - start
    print("Duration: %s" % (duration))
    print("Distance: %.2f km" % (distance/1000.0))

    s   = [i for i in speed if i is not None]
    vs  = [i for i in vertical_speed if i is not None]
    hr  = [i for i in heartrate if i is not None]
    c   = [i for i in cadence if i is not None]

    if hr:
        hr_tss, hr_avg, hr_max, hr_min = get_hrTSS(hr, duration.total_seconds(), user.hr_ftp)
        print("Heartrate: TSS: %.1f, AVG: %d, MAX: %d, MIN: %d" % (hr_tss, hr_avg, hr_max, hr_min))

    if speed:
        tss, NP, IFactor = get_TSS(s, vs, len(speed), user.ftp)
        print("Running:   TSS: %.1f" % (tss))
        print("            IF: %.2f" % (IFactor))
        print("            NP: %.2f min/km" % (16.667/NP))
        if hr:
            ng = 16.667/NP
            ngs = 1000*(60/ng)/60 # meters per minute
            print("         NP:HR: %.2f" % (ngs/hr_avg))

    if c:
        print("Cadence:   AVG: %d, MAX: %d" % (average(cadence), max(c)))

if __name__ == "__main__":
    main(sys.argv[1:])
