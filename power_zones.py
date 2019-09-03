#!/usr/bin/env python3

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

import sys, argparse

def sweetspot(ftp):
    print("Sweetspot: %d W - %d W (88%% - 93%%)" % (0.88*ftp, 0.93*ftp))

def threshold_under_overs(ftp):
    print("Threshold\nunder/over: %d/%d W" % (0.9*ftp, 1.1*ftp))

def compute_zones(ftp, lthr):
    min_pow = 0
    max_pow = 2000
    
    z1_p = 0.56*ftp
    z2_p = 0.76*ftp
    z3_p = 0.91*ftp
    z4_p = 1.06*ftp
    z5_p = 1.21*ftp
    z6_p = 1.50*ftp

    z1_hr = 0.81*lthr
    z2_hr = 0.86*lthr
    z3_hr = 0.93*lthr
    z4_hr = 0.99*lthr
    z5_hr = 1.00*lthr
    z6_hr = 1.06*lthr

    print("Zone 1: %3d - %d W (     <55%%),     - %d bpm" % (min_pow, z1_p, z1_hr))
    print("Zone 2: %d - %d W (55%% - 75%%), %d - %d bpm" % (z1_p + 1, z2_p, z1_hr + 1, z2_hr))
    print("Zone 3: %d - %d W (76%% - 90%%), %d - %d bpm" % (z2_p + 1, z3_p, z2_hr + 1, z3_hr))
    print("Zone 4: %d - %d W (91%% - 105%%), %d - %d bpm" % (z3_p + 1, z4_p, z3_hr + 1, z4_hr))
    print("Zone 5: %d - %d W (106%% - 120%%), %d - %d bpm" % (z4_p + 1, z5_p, z4_hr + 1, z5_hr))
    print("Zone 6: %d - %d W (121%% - 150%%), %d - %d bpm" % (z5_p + 1, z6_p, z5_hr + 1, z6_hr))
    print("Zone 7: >%d W (>150%%), >%d bpm" % (z6_p + 1, z6_hr + 1))
    print("")

def main(argv):
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--ftp", type=int, default=290, help="FTP power")
    parser.add_argument("-r", "--lthr", type=int, default=158, help="Lactate threshold HR")

    args = parser.parse_args()

    print("FTP: %d W" % args.ftp)
    print("LTHR: %d bpm" % args.lthr)
    print("")

    compute_zones(args.ftp, args.lthr)
    threshold_under_overs(args.ftp)
    sweetspot(args.ftp)

if __name__ == "__main__":
        main(sys.argv[1:])
