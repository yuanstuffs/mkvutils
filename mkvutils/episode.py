import re


def extract_episode_tag(filename: str) -> str:
    """
    Extracts 'SxxExx' OR simple episode numbers (e.g. '- 01') from filename.
    Examples:
      '[Judas] ... S01E01.mkv' -> 'S01E01'
      '[Erai-raws] ... - 01 [1080p...].mkv' -> 'E01'
    """
    # Case 1: SxxExx
    match = re.search(r"(S\d{2}E\d{2})", filename, re.IGNORECASE)
    if match:
        return match.group(1).upper()

    # Case 2: match " - 01" or "Ep01"
    match = re.search(r"[-_\s]\s?(\d{2})(?:\D|$)", filename)
    if match:
        return f"E{match.group(1)}"  # Normalize as E01, E02, etc.

    # raise ValueError(f"❌ No episode tag found in filename: {filename}")
    return filename
