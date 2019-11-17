#!/usr/bin/env python3
import time
import os
import shutil
import exifread
import ipdb
import fire


def main(source, output_type="jpg", destination=None, move=False):
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
    ending_length = len(output_type)
    pics = [
        os.path.join(source, f)
        for f in os.listdir(source)
        if f[-ending_length - 1 :].upper() == ".{}".format(output_type.upper())
    ]

    print(len(pics), "pics found")

    dates = sorted(
        list(
            set(
                [
                    time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(pic)))
                    for pic in pics
                ]
            )
        )
    )

    for date in dates:
        save_dir = os.path.join(destination, date, output_type)
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
        date_path = time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(pic)))
        last_slash_index = pic.rfind("/")
        pic_without_path = pic[last_slash_index + 1 :]
        dest_path = os.path.join(destination, date_path, output_type)
        if os.path.exists(os.path.join(dest_path, pic_without_path)):
            print("Uh oh, file {} already exists".format(pic_without_path))
        else:
            if move:
                print(
                    "Moving file {} to {}".format(
                        pic[last_slash_index + 1 :], dest_path
                    )
                )
                shutil.move(pic, dest_path)
            else:
                print(
                    "copying file {} to {}".format(
                        pic[last_slash_index + 1 :], dest_path
                    )
                )
                shutil.copy2(pic, dest_path)


if __name__ == "__main__":
    fire.Fire(main)
