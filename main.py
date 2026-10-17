from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase

from GUI import gui

app = QApplication()
QFontDatabase.addApplicationFont("GUI/assets/Oswald-VariableFont_wght.ttf")

window = gui.MainWindow()

window.showMaximized()

app.exec()
