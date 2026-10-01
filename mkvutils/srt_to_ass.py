import re

SRT_TIME_RE = re.compile(
    r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})"
)


def _srt_time_to_ass(h: str, m: str, s: str, ms: str) -> str:
    """SRT uses H:MM:SS,mmm (milliseconds); ASS uses H:MM:SS.cc (centiseconds)."""
    centiseconds = int(ms) // 10
    return f"{int(h)}:{m}:{s}.{centiseconds:02d}"


def _convert_tags(text: str) -> str:
    """Maps the handful of HTML-ish tags SRT allows to ASS override tags."""
    text = re.sub(
        r"<b>(.*?)</b>", r"{\\b1}\1{\\b0}", text, flags=re.IGNORECASE | re.DOTALL
    )
    text = re.sub(
        r"<i>(.*?)</i>", r"{\\i1}\1{\\i0}", text, flags=re.IGNORECASE | re.DOTALL
    )
    text = re.sub(
        r"<u>(.*?)</u>", r"{\\u1}\1{\\u0}", text, flags=re.IGNORECASE | re.DOTALL
    )
    text = re.sub(r"</?font[^>]*>", "", text, flags=re.IGNORECASE)
    return text


def parse_srt(content: str):
    """Parses SRT text into a list of (ass_start, ass_end, ass_text) tuples."""
    blocks = re.split(r"\n\s*\n", content.strip())
    entries = []

    for block in blocks:
        lines = block.strip().splitlines()
        if not lines:
            continue

        idx = 0
        if lines[0].strip().isdigit():  # skip the numeric index line, if present
            idx = 1

        if idx >= len(lines):
            continue

        time_match = SRT_TIME_RE.search(lines[idx])
        if not time_match:
            continue

        h1, m1, s1, ms1, h2, m2, s2, ms2 = time_match.groups()
        start = _srt_time_to_ass(h1, m1, s1, ms1)
        end = _srt_time_to_ass(h2, m2, s2, ms2)

        text_lines = lines[idx + 1 :]
        text = "\\N".join(
            _convert_tags(line.strip()) for line in text_lines if line.strip()
        )

        if text:
            entries.append((start, end, text))

    return entries


# Default style matches the exact field order fix_style_line() in subtitles.py expects,
# so --fontsize continues to work after conversion.
ASS_HEADER = """[Script Info]
Title: Converted from SRT
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,18,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def srt_to_ass(srt_path: str, ass_path: str) -> str:
    """
    Converts an SRT file's content into ASS format, writing to ass_path
    (can be the same path as srt_path to convert in place). Returns ass_path.
    """
    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    entries = parse_srt(content)

    lines = [ASS_HEADER]
    for start, end, text in entries:
        lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return ass_path
