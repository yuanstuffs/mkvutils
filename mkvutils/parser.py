import argparse
from dataclasses import dataclass
from typing import Literal


@dataclass
class Args:
    """
    A container for the command-line arguments.
    """

    all: bool
    file: str
    fontsize: int
    keep_subs: bool
    keep_trackname: bool
    trackid: int
    type: Literal["old", "new"]


def get_args() -> Args:
    """
    Parses command-line arguments and returns a typed object.
    """
    parser = argparse.ArgumentParser(description="Process MKV and subtitles.")
    parser.add_argument(
        "file", nargs="?", help="Input MKV file (ignored if --all is used)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all MKV files in the current directory",
    )
    parser.add_argument(
        "--fontsize", type=int, default=18, help="Font size for subtitles (default: 18)"
    )
    parser.add_argument(
        "--keep-subs",
        action="store_true",
        help="Whether to keep the extracted subtitles",
    )
    parser.add_argument(
        "--keep-trackname",
        action="store_true",
        help="Whether to keep the original track name",
    )
    parser.add_argument("--trackid", type=int, default=2, help="Track ID (default: 2)")
    parser.add_argument(
        "--type",
        type=str,
        choices=["old", "new"],
        default="new",
        help="Type of the mkv video. (default: new)",
    )

    namespace = parser.parse_args()

    return Args(**vars(namespace))
