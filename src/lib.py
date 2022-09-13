import os
import platform
import subprocess
from os import path


def _explorer_path() -> str | None:
    return path.join(os.getenv("WINDIR"), "explorer.exe") if os.getenv("WINDIR") else None


def can_find_explorer() -> bool:
    return bool(platform.system() == "Windows" and _explorer_path() and path.exists(_explorer_path()))


def explore_to_file(file_path: str) -> None:
    if not can_find_explorer():
        raise Exception("Cannot find Windows Explorer")
    subprocess.Popen((_explorer_path(), "/select,", file_path))
