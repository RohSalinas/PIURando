
from pathlib import Path
from PySide6.QtCore import QUrl

# This file is inside GUI/, so its parent is the GUI folder.
GUI_DIR = Path(__file__).resolve().parent
ASSET_DIR = GUI_DIR / "assets"


def asset_path(filename: str) -> Path:
    """Return the absolute path to a bundled GUI asset."""
    return ASSET_DIR / filename


# def asset_url(filename: str) -> str:
#     """Return a file URL suitable for a Qt stylesheet."""
#     return QUrl.fromLocalFile(
#         str(asset_path(filename).resolve())
#     ).toString()

def asset_url(filename: str) -> str:
    return asset_path(filename).resolve().as_posix()
