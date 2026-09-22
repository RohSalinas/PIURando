from PySide6.QtWidgets import QApplication

from GUI import gui

app = QApplication()

window = gui.MainWindow()

window.show()

app.exec()
