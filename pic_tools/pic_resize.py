#!/usr/bin/python

import argparse
import argcomplete
import sys
from plumbum.cmd import convert
import os

parser=argparse.ArgumentParser(description="Resize Pics", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("source", nargs="*", help="Pictures to convert")
parser.add_argument("--newsize", default=[1600, 1200], type=int, nargs=2, help="Pictures to convert")
parser.add_argument("--ending", default="_small", help="Ending for resized pics")
parser.add_argument("--verbose", "-v", action="store_true", help="Verbosity")
argcomplete.autocomplete(parser)
args = parser.parse_args()

if len(args.source) > 0:
    pics = args.source
else:
    pics = sys.stdin.read().split()
    print len(pics)

for pic in pics:
    if args.verbose == True:
        print "Converting", pic
    fn, ending = os.path.splitext(pic)
    newname = fn + args.ending + ending
    i = 1
    while os.path.exists(newname):
        newname = "{}{}{:02d}{}".format(fn, args.ending, i, ending)
    convert["{} -resize {}x{} {}".format(pic, args.newsize[0], args.newsize[1], newname).split()]()
