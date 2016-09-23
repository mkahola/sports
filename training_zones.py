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

import sys, argparse

def hr_zones_karvonen(max_hr, rest_hr):
    
        zones = ['Active recovery', 'Endurance', 'Tempo', 'Threshold', 'VO2max']

        if max_hr is None:
            print("Max heartrate not a number")
            return

        if rest_hr is None:
            print("Rest heartrate not a number")
            return

        if rest_hr > max_hr:
            print("Rest heartrate cannot be higher than max heartrate")
            return
        
        hr_reserve = max_hr - rest_hr
        
        print("Max heartrate (bpm): %3d" % max_hr)
        print("Rest heartrate (bpm): %2d" % rest_hr)
        print("Heartrate reserve: %3d\n" % hr_reserve)
        
        for i in range(0, len(zones)):
            n = 0.5 + i/10.0
            
            if i < (len(zones)-1):
                upper_limit = hr_reserve - 1
            else:
                upper_limit = hr_reserve
                
            print("Zone %d (bpm): %3d-%3d (%s)" %
                  (i+1,int(n*float(hr_reserve))+rest_hr,int((n+0.1)*upper_limit)+rest_hr, zones[i]))

def hr_zones_max_heartrate(max_hr):

    zones = ['Active recovery', 'Endurance', 'Tempo', 'Threshold', 'VO2max']
    
    if max_hr is None:
        print("Max heartrate not a number")
        return

    print("Max heartrate (bpm): %3d\n" % max_hr)

    for i in range(0, len(zones)):
        n = 0.5 + i/10.0
        
        if i < (len(zones)-1):
            upper_limit = max_hr - 1
        else:
            upper_limit = max_hr
            
        print("Zone %d (bpm): %3d-%3d (%s)" %
              (i+1,int(n*float(max_hr)),int((n+0.1)*upper_limit), zones[i]))

def main(argv):
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--method", choices=['max-heartrate', 'karvonen'], help="training zone method")
    parser.add_argument("-r", "--maxhr", type=int, help="max heartrate")
    parser.add_argument("-s", "--resthr", type=int, help="rest heartrate")

    args = parser.parse_args()

    if args.method == 'max-heartrate':
        hr_zones_max_heartrate(args.maxhr)
    elif args.method == 'karvonen':
        hr_zones_karvonen(args.maxhr, args.resthr)
    else:
        parser.print_help()
        
if __name__ == "__main__":
        main(sys.argv[1:])
