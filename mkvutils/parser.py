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
    fix_subs: bool
    fontsize: int
    force: bool
    keep_subs: bool
    keep_trackname: bool
    only_default_audio: bool
    out: str | None
    trackid: int | None


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
        "--fix-subs",
        action="store_true",
        help=(
            "Extract the subtitle track and fix its font size/style (converting SRT to "
            "ASS first if needed), then re-mux it. Without this flag, the existing "
            "subtitle track is kept exactly as-is via --trackid."
        ),
    )
    parser.add_argument(
        "--fontsize", type=int, default=18, help="Font size for subtitles (default: 18)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output file if it already exists, instead of appending -1, -2, etc.",
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
    parser.add_argument(
        "--only-default-audio",
        action="store_true",
        help="If the source has multiple audio tracks, keep only the one flagged as default",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help=(
            "Where to write output. A directory (e.g. '.', './finished/') writes files there "
            "with their original names. A path with a filename+extension (e.g. './a/a.mkv') "
            "writes the single output file there — only valid without --all. "
            "If omitted, writes to an 'out' subdirectory next to the input file."
        ),
    )
    parser.add_argument(
        "--trackid",
        type=int,
        default=None,  # was: default=2
        help="Subtitle track ID to keep (default: auto-detect English subtitle track)",
    )

    namespace = parser.parse_args()

    return Args(**vars(namespace))
