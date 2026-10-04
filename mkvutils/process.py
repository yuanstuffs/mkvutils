import subprocess

from os import makedirs, path, remove, replace as os_replace
from typing import Any, List, Optional
from constants import MKVTools
from colorize import Color, colorize
from tracks import find_default_audio_track_id
from fsutils import unique_output_path


def process_mkv(
    input_file: str,
    track_id: int,
    fix_subs: bool = False,
    keep_subs: bool = False,
    only_default_audio: bool = False,
    output_dir: Optional[str] = None,
    output_filename: Optional[str] = None,
    force: bool = False,
    subtitle_file: Optional[str] = None,
):
    if not path.isfile(input_file):
        raise FileNotFoundError(f"❌ File not found: {input_file}")

    baseout_dir = (
        output_dir if output_dir else path.join(path.dirname(input_file), "out")
    )
    makedirs(baseout_dir, exist_ok=True)

    target_filename = output_filename if output_filename else path.basename(input_file)

    if force:
        output_file = path.join(baseout_dir, target_filename)
        if path.isfile(output_file):
            print(
                colorize(f"⚠️  Overwriting existing file: {output_file}", Color.Yellow)
            )
    else:
        output_file = unique_output_path(baseout_dir, target_filename)

    # detect when the resolved output path is the same file as the input.
    # mkvmerge can't safely read from and write to the same path at once —
    # mux to a temp file instead, then move it into place once done.
    writing_over_source = path.normcase(path.abspath(output_file)) == path.normcase(
        path.abspath(input_file)
    )
    final_output_file = output_file
    if writing_over_source:
        output_file = output_file + ".tmp"
        print(
            colorize(
                f"⚠️  Output path matches input path — muxing to a temporary file first: {output_file}",
                Color.Yellow,
            )
        )

    final_command: List[Any] = [MKVTools.Merge, "-o", output_file]

    if only_default_audio:
        default_audio_id = find_default_audio_track_id(input_file)
        if default_audio_id is not None:
            final_command += ["-a", str(default_audio_id)]

    if fix_subs:
        if subtitle_file is None or not path.isfile(subtitle_file):
            raise FileNotFoundError(
                f"❌ Subtitle file not found: {colorize(str(subtitle_file), Color.Yellow)}"
            )
        final_command += ["-S", input_file, subtitle_file]
    else:
        final_command += ["-s", str(track_id), input_file]

    print(f"👉 Running merge: {colorize(' '.join(final_command), Color.Yellow)}")
    subprocess.run(final_command, check=True)

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

    # now that mkvmerge/mkvpropedit are done reading the original file,
    # it's safe to replace it with the muxed result.
    if writing_over_source:
        os_replace(output_file, final_output_file)
        output_file = final_output_file

    print(f"✅ Final file: {colorize(output_file, Color.Yellow)}")

    if subtitle_file is not None and not keep_subs and path.isfile(subtitle_file):
        remove(subtitle_file)
