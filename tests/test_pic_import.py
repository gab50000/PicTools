from datetime import date, datetime
import random
from string import ascii_lowercase

import pytest

from pic_tools.pic_import import main


def random_date(low: str, high: str):
    timestamp_low = datetime.strptime(low, "%Y-%M-%d").timestamp()
    timestamp_high = datetime.strptime(high, "%Y-%M-%d").timestamp()
    rand_date = date.fromtimestamp(
        random.randint(int(timestamp_low), int(timestamp_high))
    )
    return rand_date


def random_filename():
    rdate = random_date("2020-01-01", "2020-01-31")
    rsuffix = "".join(random.choices(ascii_lowercase, k=8))
    return f"{rdate}-{rsuffix}.jpg"


def test_copying(tmp_path, monkeypatch):
    def mock_get_date(path, exif=False):
        return path.stem[:-9]

    monkeypatch.setattr("pic_tools.pic_import.get_creation_date", mock_get_date)

    source_path = tmp_path / "source"
    source_path.mkdir()
    dest_path = tmp_path / "destination"
    dest_path.mkdir()

    for _ in range(100):
        p = source_path / random_filename()
        p.touch()

    main(source_path, dest_path)

    assert len([p for p in dest_path.rglob("*") if p.is_file()]) == 100

    for pic in dest_path.rglob("*.jpg"):
        assert pic.name.startswith(pic.parent.parent.name)
