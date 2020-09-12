#!/usr/bin/env python3
import time
import os
import pathlib
import shutil
import exifread
import fire


def get_creation_date(path):
    return time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(path)))


def main(source, destination, output_type="jpg", move=False):
    """
    Import Pictures from card and save them in folders, one for each day

    Arguments:
        destination: str
            Destination folder
        output_type: str
            Picture type
        move: bool
            Move pictures instead of copying them
    """
    source = pathlib.Path(source)
    destination = pathlib.Path(destination)
    ending_length = len(output_type)
    pics = [
        source / f
        for f in os.listdir(source)
        if f[-ending_length - 1 :].upper() == ".{}".format(output_type.upper())
    ]

    print(len(pics), "pics found")

    dates = sorted(list(set([get_creation_date(pic) for pic in pics])))

    for date in dates:
        save_dir = destination / date
        if os.path.exists(save_dir):
            print("Uh oh, path {} already existing".format(save_dir))
        else:
            print("I will create a directory", save_dir)
            os.makedirs(save_dir)

    if move:
        print("Moving files...")
    else:
        print("Copying files...")

    for pic in pics:
        date_path = get_creation_date(pic)
        dest_path = destination / date_path / output_type
        dest_path.mkdir(parents=True, exist_ok=True)
        dest_file = dest_path / pic.name

        if dest_file.exists():
            print("Uh oh, file {} already exists".format(dest_file))
            continue

        if move:
            print("Moving file {} to {}".format(pic, dest_file))
            shutil.move(pic, dest_file)
        else:
            print("copying file {} to {}".format(pic, dest_file))
            shutil.copy2(pic, dest_file)


def cli():
    fire.Fire(main)


if __name__ == "__main__":
    cli()
