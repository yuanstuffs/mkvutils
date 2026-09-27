import sys
import os

from glob import glob

from episode import extract_episode_tag
from colorize import Color, colorize, enable_ansi_on_windows
from fsutils import resolve_output
from parser import get_args
from process import process_mkv
from subtitles import extract_subs, process_sub
from tracks import find_subtitle_track_id


def resolve_trackid(file: str, args_trackid) -> int:
    return args_trackid if args_trackid is not None else find_subtitle_track_id(file)


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

    # Validate --out shape once, up front, so batch + explicit-filename fails fast
    if args.all and args.out:
        try:
            resolve_output(args.out, "placeholder.mkv", is_batch=True)
        except ValueError as e:
            print(colorize(str(e), Color.Red))
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
                trackid = resolve_trackid(file, args.trackid)
                output_dir, output_filename = resolve_output(
                    args.out, file, is_batch=True
                )
                process_sub(
                    extract_subs(
                        file,
                        episode_tag=episode_tag,
                        track_id=trackid,
                        output_dir=output_dir,
                    ),
                    fontsize=args.fontsize,
                )
                process_mkv(
                    file,
                    track_id=trackid,
                    action_type=args.type,
                    episode_tag=episode_tag,
                    keep_subs=args.keep_subs,
                    only_default_audio=args.only_default_audio,
                    output_dir=output_dir,
                    output_filename=output_filename,
                    force=args.force,
                )
        else:
            print(colorize("Running 'old' handler.", Color.Blue))
            episode_tag = extract_episode_tag(os.path.basename(input_file))
            trackid = resolve_trackid(input_file, args.trackid)
            output_dir, output_filename = resolve_output(
                args.out, input_file, is_batch=False
            )
            process_sub(
                extract_subs(
                    input_file,
                    episode_tag=episode_tag,
                    track_id=trackid,
                    output_dir=output_dir,
                ),
                fontsize=args.fontsize,
            )
            process_mkv(
                input_file,
                track_id=trackid,
                action_type=args.type,
                episode_tag=episode_tag,
                keep_subs=args.keep_subs,
                only_default_audio=args.only_default_audio,
                output_dir=output_dir,
                output_filename=output_filename,
                force=args.force,
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
                trackid = resolve_trackid(file, args.trackid)
                output_dir, output_filename = resolve_output(
                    args.out, file, is_batch=True
                )
                process_mkv(
                    file,
                    track_id=trackid,
                    action_type=args.type,
                    keep_subs=args.keep_subs,
                    only_default_audio=args.only_default_audio,
                    output_dir=output_dir,
                    output_filename=output_filename,
                    force=args.force,
                )
        else:
            print(colorize("Running 'new' handler.", Color.Blue))
            trackid = resolve_trackid(input_file, args.trackid)
            output_dir, output_filename = resolve_output(
                args.out, input_file, is_batch=False
            )
            process_mkv(
                input_file,
                track_id=trackid,
                action_type=args.type,
                keep_subs=args.keep_subs,
                only_default_audio=args.only_default_audio,
                output_dir=output_dir,
                output_filename=output_filename,
                force=args.force,
            )


if __name__ == "__main__":
    main()
