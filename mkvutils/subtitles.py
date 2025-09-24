import subprocess

from os import path, makedirs
from constants import MKVTools
from colorize import Color, colorize


def extract_subs(input_file: str, episode_tag: str, track_id: int) -> str:
    """Extracts subs from MKV → ./out/subs.SxxExx.ass"""
    basedir = path.join(path.dirname(input_file), "out")
    makedirs(basedir, exist_ok=True)
    output_file = path.join(basedir, f"subs.{episode_tag}.ass")

    cmd = [MKVTools.Extract, "tracks", input_file, f"{track_id}:{output_file}"]

    print(f"👉 Extracting subs: {colorize(' '.join(cmd), Color.Yellow)}")
    subprocess.run(cmd, check=True)

    print(f"✅ Extracted: {colorize(output_file, Color.Yellow)}")
    return output_file


# Not exported
def fix_style_line(line: str, fontsize: int) -> str:
    parts = line.split(",")
    if len(parts) < 23:
        return line  # not a valid style line

    # print(dict(enumerate(parts)))
    # Force font size = 18
    print("File original fontsize: {}".format(colorize(parts[2], Color.Green)))
    parts[2] = str(fontsize)
    print("Changed fontsize: {}".format(colorize(parts[2], Color.Green)))
    parts[15] = "1"
    # Force outline = 0 (index 16)
    parts[16] = "2"
    # Force shadow = 0 (index 17)
    parts[17] = "0"
    parts[18] = "2"

    return ",".join(parts)


def process_sub(input_file: str, fontsize: int):
    # Make output name by adding -mod before extension
    base, ext = path.splitext(input_file)
    output_file = f"{base}{ext}"

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    fixed_lines = []
    for line in lines:
        if line.startswith("Style:"):
            fixed_lines.append(fix_style_line(line.strip(), fontsize) + "\n")
        else:
            fixed_lines.append(line)

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(fixed_lines)

    print(f"✅ Processed: {colorize(input_file, Color.Yellow)}")
    print(f"👉 Saved as: {colorize(output_file, Color.Yellow)}")
