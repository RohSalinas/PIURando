from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QIcon
from GUI.resource_paths import asset_path

from GUI import gui

ASSET_DIR = Path(__file__).resolve().parent / "GUI" / "assets"

app = QApplication()
app.setWindowIcon(QIcon(str(asset_path("icon_tr.ico"))))

QFontDatabase.addApplicationFont(
    str(ASSET_DIR / "Oswald-VariableFont_wght.ttf")
)

window = gui.MainWindow()

window.showMaximized()

app.exec()
