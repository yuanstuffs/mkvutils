import subprocess

from os import makedirs, path
from typing import Any, List, Literal, Optional
from constants import MKVTools
from colorize import Color, colorize


def process_mkv(
    input_file: str,
    track_id: int = 2,
    action_type: Optional[Literal["old", "new"]] = None,
    episode_tag: Optional[str] = None,
):
    if not path.isfile(input_file):
        raise FileNotFoundError(f"❌ File not found: {input_file}")

    # Output filename in ./out/
    baseout_dir = path.join(path.dirname(input_file), "out")
    makedirs(baseout_dir, exist_ok=True)
    output_file = path.join(baseout_dir, path.basename(input_file))

    final_command: List[Any] = []

    # Step 1: merge keeping only video/audio, add English subtitles
    # (-S removes all subtitles from the source)
    if action_type == "old":
        subtitle_file: str
        # Subtitle file in ./subs/
        subtitle_file = path.join(
            path.join(path.dirname(input_file), "subs"), f"{episode_tag}.ass"
        )

        if not path.isfile(subtitle_file):
            alternative_filename = path.join(
                path.join(path.dirname(input_file), "subs"), f"{input_file}.ass"
            )

            if not path.isfile(alternative_filename):
                raise FileNotFoundError(
                    f"❌ Subtitle file not found: {colorize(subtitle_file, Color.Yellow)}"
                )

            subtitle_file = alternative_filename

        final_command = [
            MKVTools.Merge,
            "-o",
            output_file,
            "-S",
            input_file,
            subtitle_file,
        ]
    else:
        final_command = [
            MKVTools.Merge,
            "-o",
            output_file,
            "-s",
            str(track_id),
            input_file,
        ]

    print(f"👉 Running merge: {colorize(' '.join(final_command), Color.Yellow)}")
    subprocess.run(final_command, check=True)

    # Step 2: ensure English track metadata is set correctly
    cmd_edit = [
        MKVTools.ProPedit,
        output_file,
        "--edit",
        "track:s1",
        "--set",
        "name=English",
        "--set",
        "language=eng",
        "--set",
        "flag-default=1",
    ]
    print(f"👉 Running track edit: {colorize(' '.join(cmd_edit), Color.Yellow)}")
    subprocess.run(cmd_edit, check=True)

    print(f"✅ Final file: {colorize(output_file, Color.Yellow)}")
