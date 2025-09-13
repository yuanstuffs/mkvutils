import os
import sys


class Color:
    Red = "\033[91m"
    Green = "\033[92m"
    Yellow = "\033[93m"
    Blue = "\033[94m"
    Reset = "\033[0m"


# Add an effect
class Style:
    Bold = "\033[1m"
    Reset = "\033[0m"


def colorize(text, color_code):
    return f"{color_code}{text}{Color.Reset}"


def enable_ansi_on_windows():
    """
    Enables ANSI escape codes on Windows versions that require it.
    This uses the standard library and requires no external dependencies.
    """
    if os.name == "nt":  # Check if the OS is Windows
        try:
            import ctypes

            # Get a handle to the standard output
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            # Get the current console mode
            mode = ctypes.c_ulong(0)
            ctypes.windll.kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            # Enable ENABLE_VIRTUAL_TERMINAL_PROCESSING (0x0004)
            ctypes.windll.kernel32.SetConsoleMode(handle, mode.value | 4)
        except Exception as e:
            # Fallback for systems that fail to enable ANSI
            print(f"Warning: Failed to enable ANSI on Windows. {e}", file=sys.stderr)
