#!/usr/bin/env python2

"""
Copyright (c) 2017

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

# requires python-fitparse library from
# https://github.com/dtcooper/python-fitparse
from fitparse import FitFile, FitParseError
from scipy.signal import lfilter

def get_hrTSS(hr, duration, threshold):

    if not hr:
        return 0, 0, 0, 0

    hr_avg = sum(hr)/float(len(hr))
    hr_min = min(hr)
    hr_max = max(hr)
    tss = (duration * hr_avg)/(threshold * 3600.0) * 100.0

    return tss, hr_avg, hr_max, hr_min

def get_TSS(power, duration, ftp):
    if not power:
        return 0, 0, 0

    # 30s moving average filter
    h = numpy.empty(30)
    h.fill(1.0/30)

    # power of 4 of 30s average power
    p_30s = lfilter(h, 1.0, power)**4

    # average of power of 4
    try:
        p_avg = sum(p_30s)/float(len(p_30s))
    except ZeroDivisionError:
        print("divide by zero")
        p_avg = 0

    # normalized power
    NP = math.sqrt(math.sqrt(p_avg))

    # intensity factor
    IFactor = NP/float(ftp)

    # training stress score as in trainingpeaks.com
    tss = (duration * NP * IFactor) / (ftp * 3600.0) * 100.0
    
    return tss, NP, IFactor

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fitfile", type=str, default="", help="FIT file")
    parser.add_argument("-p", "--ftp",   type=int, default=287, help="Functional Threshold Power")
    parser.add_argument("-t", "--threshold", type=int, default=155, help="Heartrate threshold")
    args = parser.parse_args()

    try:
        fitfile = FitFile(args.fitfile)
        fitfile.parse()
    except FitParseError, e:
        print "Error while parsing .FIT file: %s" % e
        sys.exit(1)
    
    power = []
    heartrate = []
    # Get all data messages that are of type record
    for record in fitfile.get_messages('record'):
        
        # Go through all the data entries in this record
        for data in record:
            if data.name == "power":
                power.append(data.value)
            if data.name == "heart_rate":
                heartrate.append(data.value)

    p  = [i for i in power if i is not None]
    hr = [i for i in heartrate if i is not None]

    try:
        Pavg = sum(filter(None, power))/float(len(filter(None, power)))
    except ZeroDivisionError:
        print("divide by zero")
        Pavg = 0

    tss, NP, IFactor = get_TSS(p, len(power), args.ftp)
    if not p:
        Pmax = 0
    else:
        Pmax = max(p)

    hr_tss, hr_avg, hr_max, hr_min = get_hrTSS(hr, len(heartrate), args.threshold)

    print("Power:     TSS: %.1f, IF: %.2f, NP: %d W, AVG: %d W, MAX: %d W" % (tss, IFactor, NP, Pavg, Pmax))
    print("Heartrate: TSS: %.1f, AVG: %d, MAX: %d, MIN: %d" % (hr_tss, hr_avg, hr_max, hr_min))

if __name__ == "__main__":
    main(sys.argv[1:])
