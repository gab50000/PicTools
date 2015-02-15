#!/usr/bin/python

import argparse
import time
import os
import shutil

def main(*args):
	pass
	
if __name__ == "__main__":
	parser=argparse.ArgumentParser(description="Import Pictures from card and save them in folders, one for each day", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("source", help="Source folder")
	parser.add_argument("--destination", default="/home/kabbe/Bilder/Pictures/Olympus", help="Destination folder")
	parser.add_argument("--type", default="jpg", help="Picture type")
	args = parser.parse_args()
	
	ending_length = len(args.type)
	pics = [os.path.join(args.source, f) for f in os.listdir(args.source) if f[-ending_length-1:].upper() == ".{}".format(args.type.upper())]
	
	print len(pics), "pics found"
	
	dates = sorted(list(set([time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(pic))) for pic in pics])))
	
	for date in dates:
		save_dir = os.path.join(args.destination, args.type, date)
		if os.path.exists(save_dir):
			print "Uh oh, path {} already existing".format(save_dir)
		else:
			print "I will create a directory", save_dir
			os.makedirs(save_dir)
			
	print "Copying files..."
	
	for pic in pics:
		date_path = time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(pic)))
		last_slash_index = pic.rfind("/")
		pic_without_path = pic[last_slash_index+1:]
		dest_path = os.path.join(args.destination, date_path, args.type)
		if os.path.exists(os.path.join(dest_path, pic_without_path)):
			print "Uh oh, file {} already exists".format(pic_without_path)
		else:
			print "copying file {} to {}".format(pic[last_slash_index+1:], dest_path)
			shutil.copy2(pic, dest_path)
