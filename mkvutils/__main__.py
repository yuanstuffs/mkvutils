import sys
import os

from glob import glob

from episode import extract_episode_tag
from colorize import Color, colorize, enable_ansi_on_windows
from parser import get_args
from process import process_mkv
from subtitles import extract_subs, process_sub


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

    if args.type == "old":
        if args.all:
            print(colorize("Running 'old' handler for all files.", Color.Blue))
            files = glob("*.mkv")
            if not files:
                print(
                    colorize("No MKV files found in the current directory.", Color.Red)
                )
                sys.exit(1)

            for file in files:
                print(colorize(f"Processing file: {file}", Color.Green))
                episode_tag = extract_episode_tag(os.path.basename(file))
                process_sub(
                    extract_subs(file, episode_tag=episode_tag, track_id=args.trackid),
                    fontsize=args.fontsize,
                )
                process_mkv(
                    file,
                    action_type=args.type,
                    episode_tag=episode_tag,
                    keep_subs=args.keep_subs,
                )
        else:
            print(colorize("Running 'old' handler.", Color.Blue))
            episode_tag = extract_episode_tag(os.path.basename(input_file))
            process_sub(
                extract_subs(
                    input_file, episode_tag=episode_tag, track_id=args.trackid
                ),
                fontsize=args.fontsize,
            )
            process_mkv(
                input_file,
                action_type=args.type,
                episode_tag=episode_tag,
                keep_subs=args.keep_subs,
            )
    else:
        if args.all:
            print(colorize("Running 'new' handler for all files.", Color.Blue))
            files = glob("*.mkv")
            if not files:
                print(
                    colorize("No MKV files found in the current directory.", Color.Red)
                )
                sys.exit(1)

            for file in files:
                print(colorize(f"Processing file: {file}", Color.Green))
                process_mkv(file, action_type=args.type, keep_subs=args.keep_subs)
        else:
            print(colorize("Running 'new' handler.", Color.Blue))
            process_mkv(input_file, action_type=args.type, keep_subs=args.keep_subs)


if __name__ == "__main__":
    main()
