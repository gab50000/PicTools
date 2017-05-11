#!/usr/bin/env python3
"""
Import Pictures from card and save them in folders, one for each day

Usage: 
    test.py [--destination <dest>] [--move] [--type <type>] <source>
    test.py (-h|--help)

Options:
  -h --help                   show this help message and exit
  --destination <dest>        Destination folder [default: /home/kabbe/Bilder/Olympus]
  --type <type>               Picture type [default: jpg]
  --move                      Move pictures instead of copying them [default: False]
"""
from docopt import docopt
import time
import os
import shutil
import exifread
import ipdb


def main(*args):
    args = docopt(__doc__)
    print(args)
    
    ending_length = len(args["--type"])
    pics = [os.path.join(args["<source>"], f) for f in os.listdir(args["<source>"]) if f[-ending_length-1:].upper() == ".{}".format(args["--type"].upper())]
    
    print(len(pics), "pics found")
    
    #~ for pic in pics:
        
    dates = sorted(list(set([time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(pic))) for pic in pics])))
    
    for date in dates:
        save_dir = os.path.join(args["--destination"], date, args["--type"])
        if os.path.exists(save_dir):
            print("Uh oh, path {} already existing".format(save_dir))
        else:
            print("I will create a directory", save_dir)
            os.makedirs(save_dir)
            
    if args["--move"]:
        print("Moving files...")
    else:
        print("Copying files...")
    
    for pic in pics:
        date_path = time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(pic)))
        last_slash_index = pic.rfind("/")
        pic_without_path = pic[last_slash_index+1:]
        dest_path = os.path.join(args["--destination"], date_path, args["--type"])
        if os.path.exists(os.path.join(dest_path, pic_without_path)):
            print("Uh oh, file {} already exists".format(pic_without_path))
        else:
            if args["--move"]:
                print("Moving file {} to {}".format(pic[last_slash_index+1:], dest_path))
                shutil.move(pic, dest_path)
            else:
                print("copying file {} to {}".format(pic[last_slash_index+1:], dest_path))
                shutil.copy2(pic, dest_path)

    
if __name__ == "__main__":
    main()
