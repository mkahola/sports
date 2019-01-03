#!/usr/bin/env python3

"""
Copyright (c) 2019

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

"System 5/3/1 weight computation"

import sys, argparse

def get_weight(p, max_val):
    x = int(((p*max_val)/2.5 + 0.5))

    return x*2.5

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--weight", type=float, default=120, help="max weight in kg")

    args = parser.parse_args()

    print("1RM: %.1f kg\n" % (args.weight))

    print("week 1:")
    print("\t 5x%.1f kg" % get_weight(0.65, 0.9*args.weight))
    print("\t 5x%.1f kg" % get_weight(0.75, 0.9*args.weight))
    print("\t 5x%.1f kg" % get_weight(0.85, 0.9*args.weight))

    print("week 2:")
    print("\t 3x%.1f kg" % get_weight(0.70, 0.9*args.weight))
    print("\t 3x%.1f kg" % get_weight(0.80, 0.9*args.weight))
    print("\t 3x%.1f kg" % get_weight(0.90, 0.9*args.weight))

    print("week 3:")
    print("\t 5x%.1f kg" % get_weight(0.75, 0.9*args.weight))
    print("\t 3x%.1f kg" % get_weight(0.85, 0.9*args.weight))
    print("\t 1x%.1f kg" % get_weight(0.95, 0.9*args.weight))

    print("week 4:")
    print("\t 5x%.1f kg" % get_weight(0.40, 0.9*args.weight))
    print("\t 5x%.1f kg" % get_weight(0.50, 0.9*args.weight))
    print("\t 5x%.1f kg" % get_weight(0.60, 0.9*args.weight))

    print("warmup:")
    print("\t 5x%.1f kg" % get_weight(0.40, 0.9*args.weight))
    print("\t 5x%.1f kg" % get_weight(0.50, 0.9*args.weight))
    print("\t 3x%.1f kg" % get_weight(0.65, 0.9*args.weight))
    
if __name__ == "__main__":
    main(sys.argv[1:])
