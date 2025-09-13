import sys
import os

from episode import extract_episode_tag
from markup import Color, colorize, enable_ansi_on_windows
from parser import get_args
from process import process_mkv
from subtitles import extract_subs, process_sub


def main():
    enable_ansi_on_windows()
    args = get_args()

    input_file = args.file
    if not os.path.isfile(input_file):
        print(
            colorize("Provided file is neither a file or does not exists.", Color.Red)
        )
        sys.exit(1)

    if args.type == "old":
        print(colorize("Running 'old' handler.", Color.Blue))
        episode_tag = extract_episode_tag(os.path.basename(input_file))
        process_sub(
            extract_subs(input_file, episode_tag=episode_tag, track_id=args.trackid),
            fontsize=args.fontsize,
        )
        process_mkv(input_file, action_type=args.type, episode_tag=episode_tag)
    else:
        print(colorize("Running 'new' handler.", Color.Blue))
        process_mkv(input_file, action_type=args.type)


if __name__ == "__main__":
    main()
