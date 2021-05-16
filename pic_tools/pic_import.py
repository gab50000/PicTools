#!/usr/bin/env python3
import time
import os
import pathlib
import shutil
import fire
from PIL import Image, ExifTags


def get_creation_date_from_exif(path):
    img = Image.open(path)
    # 36867: DateTimeOriginal
    return img.getexif()[36867].split()[0].replace(":", "-")


def get_creation_date(path, exif=False):
    if exif:
        try:
            return get_creation_date_from_exif(path)
        except KeyError:
            return get_creation_date(path, exif=False)

    return time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(path)))


def main(source, destination, output_type="jpg", move=False, exif=False):
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

    creation_date_per_pic = {pic: get_creation_date(pic, exif=exif) for pic in pics}
    dates = sorted(list(set(creation_date_per_pic.values())))

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
        date_path = creation_date_per_pic[pic]
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
