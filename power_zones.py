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
    print("Sweetspot %d W - %d W" % (0.88*ftp, 0.93*ftp))

def threshold_under_overs(ftp):
    print("Threshold under/over power: %d/%d W" % (0.9*ftp, 1.1*ftp))

def compute_zones(ftp):
    min_pow = 0
    max_pow = 2000
    
    z1 = 0.56*ftp
    z2 = 0.76*ftp
    z3 = 0.91*ftp
    z4 = 1.06*ftp
    z5 = 1.21*ftp
    z6 = 1.50*ftp

    print("Zone 1: %3d - %d W" % (min_pow, z1))
    print("Zone 2: %d - %d W" % (z1 + 1, z2))
    print("Zone 3: %d - %d W" % (z2 + 1, z3))
    print("Zone 4: %d - %d W" % (z3 + 1, z4))
    print("Zone 5: %d - %d W" % (z4 + 1, z5))
    print("Zone 6: %d - %d W" % (z5 + 1, z6))
    print("Zone 7: %d - %d W" % (z6 + 1, max_pow))
    print("")

def main(argv):
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--ftp", type=int, default=293, help="FTP power")

    args = parser.parse_args()

    print("FTP: %d W" % args.ftp)
    print("")

    compute_zones(args.ftp);
    threshold_under_overs(args.ftp)
    sweetspot(args.ftp)

if __name__ == "__main__":
        main(sys.argv[1:])
