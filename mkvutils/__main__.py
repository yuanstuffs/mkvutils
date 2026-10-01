import sys
import os

from glob import glob

from episode import extract_episode_tag
from colorize import Color, colorize, enable_ansi_on_windows
from fsutils import resolve_output
from parser import get_args
from process import process_mkv
from srt_to_ass import srt_to_ass
from subtitles import extract_subs, process_sub
from tracks import find_subtitle_track_id, get_track_codec

ASS_CODECS = {"S_TEXT/ASS", "S_TEXT/SSA"}
SRT_CODECS = {"S_TEXT/UTF8", "S_TEXT/ASCII"}


def handle_subtitle_file(file: str, trackid: int, subtitle_file: str, fontsize: int):
    """Converts SRT->ASS if needed, then applies the fontsize/style fix."""
    codec = get_track_codec(file, trackid)

    if codec in ASS_CODECS:
        process_sub(subtitle_file, fontsize=fontsize)
    elif codec in SRT_CODECS:
        print(
            colorize(
                f"👉 Subtitle track {trackid} is SRT ('{codec}') — converting to ASS.",
                Color.Blue,
            )
        )
        srt_to_ass(subtitle_file, subtitle_file)
        process_sub(subtitle_file, fontsize=fontsize)
    else:
        print(
            colorize(
                f"⚠️  Subtitle track {trackid} has unrecognized codec '{codec}' — skipping style edit.",
                Color.Yellow,
            )
        )


def process_single(file: str, args):
    trackid = args.trackid if args.trackid is not None else find_subtitle_track_id(file)
    output_dir, output_filename = resolve_output(args.out, file, is_batch=args.all)

    subtitle_file = None
    if args.fix_subs:
        episode_tag = extract_episode_tag(os.path.basename(file))
        subtitle_file = extract_subs(
            file, episode_tag=episode_tag, track_id=trackid, output_dir=output_dir
        )
        handle_subtitle_file(file, trackid, subtitle_file, args.fontsize)

    process_mkv(
        file,
        track_id=trackid,
        fix_subs=args.fix_subs,
        keep_subs=args.keep_subs,
        only_default_audio=args.only_default_audio,
        output_dir=output_dir,
        output_filename=output_filename,
        force=args.force,
        subtitle_file=subtitle_file,
    )


def main():
    enable_ansi_on_windows()
    args = get_args()

    input_file = args.file
    if not args.all and not input_file:
        print(colorize("No input file provided.", Color.Red))
        sys.exit(1)

    if not args.all and not os.path.isfile(input_file):
        print(
            colorize("Provided file is neither a file or does not exists.", Color.Red)
        )
        sys.exit(1)

    if args.all and args.out:
        try:
            resolve_output(args.out, "placeholder.mkv", is_batch=True)
        except ValueError as e:
            print(colorize(str(e), Color.Red))
            sys.exit(1)

    mode_label = "fix-subs" if args.fix_subs else "keep-subs-as-is"

    if args.all:
        print(colorize(f"Running for all files ({mode_label}).", Color.Blue))
        files = glob("*.mkv")
        if not files:
            print(colorize("No MKV files found in the current directory.", Color.Red))
            sys.exit(1)
        for file in files:
            print(colorize(f"Processing file: {file}", Color.Green))
            process_single(file, args)
    else:
        print(colorize(f"Running ({mode_label}).", Color.Blue))
        process_single(input_file, args)


if __name__ == "__main__":
    main()
