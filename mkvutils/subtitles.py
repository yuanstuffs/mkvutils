import subprocess

from os import path, makedirs
from constants import MKVTools
from colorize import Color, colorize


def extract_subs(
    input_file: str, episode_tag: str, track_id: int, output_dir: str | None = None
) -> str:
    """Extracts subs from MKV → <out_dir>/subs.SxxExx.ass"""
    basedir = output_dir if output_dir else path.join(path.dirname(input_file), "out")
    makedirs(basedir, exist_ok=True)
    output_file = path.join(basedir, f"subs.{episode_tag}.ass")

    cmd = [MKVTools.Extract, "tracks", input_file, f"{track_id}:{output_file}"]

    print(f"👉 Extracting subs: {colorize(' '.join(cmd), Color.Yellow)}")
    subprocess.run(cmd, check=True)

    print(f"✅ Extracted: {colorize(output_file, Color.Yellow)}")
    return output_file


# Not exported
def fix_style_line(line: str, fontsize: int, outline: int = 1, shadow: int = 0) -> str:
    parts = line.split(",")
    if len(parts) < 23:
        return line

    print("File original fontsize: {}".format(colorize(parts[2], Color.Green)))
    parts[2] = str(fontsize)
    print("Changed fontsize: {}".format(colorize(parts[2], Color.Green)))

    parts[15] = "1"  # BorderStyle

    print("File original outline: {}".format(colorize(parts[16], Color.Green)))
    parts[16] = str(outline)  # was hardcoded "2"
    print("Changed outline: {}".format(colorize(parts[16], Color.Green)))

    print("File original shadow: {}".format(colorize(parts[17], Color.Green)))
    parts[17] = str(shadow)
    print("Changed shadow: {}".format(colorize(parts[17], Color.Green)))

    parts[18] = "2"  # Alignment

    return ",".join(parts)


def process_sub(input_file: str, fontsize: int):
    # Make output name by adding -mod before extension
    base, ext = path.splitext(input_file)
    output_file = f"{base}{ext}"

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    style_lines_found = sum(1 for l in lines if l.startswith("Style:"))
    if style_lines_found == 0:
        print(
            colorize(
                f"⚠️  No 'Style:' lines found in {input_file} — nothing to edit.",
                Color.Yellow,
            )
        )
        return

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
