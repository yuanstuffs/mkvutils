from os import path, sep
from typing import Optional, Tuple


def unique_output_path(directory: str, filename: str) -> str:
    """
    Returns a path in `directory` for `filename` that doesn't collide with an
    existing file. If `directory/filename` already exists, appends '-1',
    '-2', etc. before the extension until a free name is found.
    """
    candidate = path.join(directory, filename)
    if not path.isfile(candidate):
        return candidate

    base, ext = path.splitext(filename)
    counter = 1
    while True:
        new_candidate = path.join(directory, f"{base}-{counter}{ext}")
        if not path.isfile(new_candidate):
            return new_candidate
        counter += 1


def resolve_output(
    out: Optional[str], input_file: str, is_batch: bool
) -> Tuple[str, Optional[str]]:
    """
    Interprets the --out value and returns (output_dir, explicit_filename).
    explicit_filename is None when `out` designates a directory only.

    Rules:
      - out is None            -> default '<input_dir>/out/', no explicit filename
      - out == '.'              -> directory: current working directory
      - out ends with a slash   -> directory
      - out is an existing dir  -> directory
      - out has a file extension -> directory + explicit filename (rejected if is_batch)
      - otherwise               -> treated as a directory to create
    """
    if out is None:
        return path.join(path.dirname(input_file), "out"), None

    if out == "." or out.endswith(("/", sep)) or path.isdir(out):
        return out, None

    base, ext = path.splitext(out)
    if ext:
        if is_batch:
            raise ValueError(
                f"❌ --out '{out}' looks like a specific file, but --all was used. "
                "Pass a directory (e.g. --out=./output/) when processing multiple files."
            )
        directory = path.dirname(out) or "."
        filename = path.basename(out)
        return directory, filename

    # no extension, doesn't exist yet: treat as a directory
    return out, None
