import json
import subprocess
from typing import Optional

from constants import MKVTools
from colorize import Color, colorize


def identify_tracks(input_file: str) -> dict:
    """Runs `mkvmerge -J` to get machine-readable track info for the file."""
    result = subprocess.run(
        [MKVTools.Merge, "-J", input_file],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def find_subtitle_track_id(input_file: str, preferred_lang: str = "eng") -> int:
    """
    Finds the subtitle track ID for this file, preferring one tagged as the
    given language, falling back to the first subtitle track found.
    """
    info = identify_tracks(input_file)
    subtitle_tracks = [
        t for t in info.get("tracks", []) if t.get("type") == "subtitles"
    ]

    if not subtitle_tracks:
        raise ValueError(f"❌ No subtitle tracks found in: {input_file}")

    for track in subtitle_tracks:
        if track.get("properties", {}).get("language") == preferred_lang:
            print(
                f"👉 Auto-detected {colorize(preferred_lang, Color.Green)} subtitle track: "
                f"{colorize(str(track['id']), Color.Yellow)}"
            )
            return track["id"]

    fallback = subtitle_tracks[0]["id"]
    print(
        f"⚠️  No '{preferred_lang}' subtitle track found, falling back to first "
        f"subtitle track: {colorize(str(fallback), Color.Yellow)}"
    )
    return fallback


def find_default_audio_track_id(input_file: str) -> Optional[int]:
    """
    If the source has more than one audio track, returns the ID of the one
    flagged as default. Returns None if there's only one (or zero) audio
    tracks, or if multiple exist but none is flagged default.
    """
    info = identify_tracks(input_file)
    audio_tracks = [t for t in info.get("tracks", []) if t.get("type") == "audio"]

    if len(audio_tracks) <= 1:
        return None

    for track in audio_tracks:
        if track.get("properties", {}).get("default_track"):
            print(
                f"👉 Multiple audio tracks found, using default: "
                f"{colorize(str(track['id']), Color.Yellow)}"
            )
            return track["id"]

    print(
        colorize(
            "⚠️  Multiple audio tracks found but none flagged default; keeping all.",
            Color.Yellow,
        )
    )
    return None
