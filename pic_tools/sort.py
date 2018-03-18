import argparse
from datetime import date
import pathlib

import daiquiri


logger = daiquiri.getLogger(__name__)
daiquiri.setup(level=daiquiri.logging.INFO)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Folder containing images")
    parser.add_argument("--extension", default=".JPG", help="Specifiy image extension")
    args = parser.parse_args()

    folder_path = pathlib.Path(args.folder)
    images = folder_path.glob(f"**/*{args.extension}")

    for img in images:
        creation_date = date.fromtimestamp(img.stat().st_mtime)
        new_path = folder_path / "sorted" / str(creation_date.year) / str(creation_date.month) #/ str(creation_date.day)
        if not new_path.exists():
            new_path.mkdir(parents=True)
        try:
            pathlib.os.link(img, new_path / img.name)
        except FileExistsError:
            logger.info("File already exists. Skipping..")
        logger.info("Created hard link to %s in %s", img, new_path / img.name)


if __name__ == '__main__':
    main()