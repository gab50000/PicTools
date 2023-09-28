import glob
import itertools
import logging
import os
import pathlib

import fire


logger = logging.getLogger("pic_check_completeness")


def get_all_pictures(path):
    return [
        pathlib.Path(p)
        for p in itertools.chain.from_iterable(
            (
                glob.glob(os.path.join(path, f"**/*.{ext}"), recursive=True)
                for ext in ("jpg", "JPG")
            )
        )
    ]


def check_completeness(path_to_sd_card, path_to_archive, *, log_level="info"):
    logging.basicConfig(level=getattr(logging, log_level.upper()))
    pics_on_card = get_all_pictures(path_to_sd_card)
    pics_in_archive = get_all_pictures(path_to_archive)
    pic_names_in_archive = {pic.name: pic for pic in pics_in_archive}

    logger.info("Found %i pictures on card", len(pics_on_card))
    logger.info("Found %i pictures in archives", len(pics_in_archive))

    not_found_count = 0
    for pic in pics_on_card:
        if pic.name not in pic_names_in_archive:
            logger.error("Did not find %s in archives!")
            not_found_count += 1
        else:
            logger.debug(
                "Found %s in archives: %s", pic.name, pic_names_in_archive[pic.name]
            )

    if not_found_count == 0:
        logger.info("All pictures were found in archives")
    else:
        logger.info(
            "%i/%i pictures were not found in archives",
            not_found_count,
            len(pics_on_card),
        )


def cli():
    fire.Fire(check_completeness)
