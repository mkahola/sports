#!/usr/bin/env python3

"""
Copyright (c) 2016

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

import sys, getopt

def help():
    print("Usage: hz_zones <max heartrate in bpm>\n")
          
def hr_zones(max_hr):

    zones = ['active recovery', 'endurance', 'tempo', 'threshold', 'VO2max']
    
    print("Max heartrate (bpm): %3d" % max_hr);
    
    for i in range(0, len(zones)):
        n = 0.5 + i/10.0

        if i < (len(zones)-1):
            print("zone %d (bpm): %3d-%3d (%s)" %
                  (i+1,int(n*float(max_hr)),int((n+0.1)*float(max_hr))-1, zones[i]))
        else:
            print("zone %d (bpm): %3d-%3d (%s)" %
                  (i+1,int(n*float(max_hr)),int((n+0.1)*float(max_hr)), zones[i]))          
        
def main(argv):
    
    if not argv:
        return

    if argv.isnumeric():
        max_hr = int(argv)
    else:
        print("input is not a number!")
        help()
        return

    if not (100 <= max_hr <= 220):
        print("Max heartrate not in range between 100 to 220 bpm")
        return
    
    hr_zones(max_hr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("max heartrate missing!")
        help()
    else:
        main(sys.argv[1])
