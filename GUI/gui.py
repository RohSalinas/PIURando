from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QCheckBox, QMessageBox, QProgressBar, QDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread

from api.api_functions import randomize_button
from api.api_maincall import delete_cache, get_charts_info, CacheWorker

from GUI.texts import cacheText
from pathlib import Path


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(640, 320)

        # Menu Bar
        self.setWindowTitle("Pump it Up - Song Randomizer")

        menubar = self.menuBar()

        fileMenu = menubar.addMenu("File")

        # =========
        # Cache
        # =========

        layout_cache = QHBoxLayout()

        cacheSubMenu = fileMenu.addMenu("Cache")
        cacheReloadCache = cacheSubMenu.addAction("Reload Song Cards Cache")
        cacheDeleteCache = cacheSubMenu.addAction("Delete Song Cards Cache")

        self.cacheProgressBar = QProgressBar()
        self.cacheProgressBar.setRange(0, 100)

        layout_cache.addWidget(self.cacheProgressBar)

        # =========
        exitAction = fileMenu.addAction("Exit")

        helpMenu = menubar.addMenu("Help")
        aboutAction = helpMenu.addAction("About")

        # Menu Triggers
        exitAction.triggered.connect(self.close)
        aboutAction.triggered.connect(lambda: QMessageBox.information(self,
                                                                      "About Pump it Up Randomizer",
                                                                      "Work in progress by RoHiSakk"))

        cacheReloadCache.triggered.connect(self.cacheReload_yes_no)
        cacheDeleteCache.triggered.connect(self.cacheDelete_yes_no)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        main_layout = QVBoxLayout(central_widget)

        # =================

        # Sub: Central Song Art Image
        layout_songart = QGridLayout()

        wg_songart = QLabel(self)
        pixmap = QPixmap("placeholder.jpg")
        wg_songart.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        wg_songart.setAlignment(Qt.AlignCenter)

        layout_songart.addWidget(wg_songart, 0, 0)

        # =================

        # Sub: Main Settings
        layout_MainSettings = QHBoxLayout()

        wg_modetext = QLabel("Mode")

        wg_mode = QComboBox()
        wg_mode.addItems(["Single", "Double", "Co-Op"])

        wg_leveltext = QLabel("From Level")

        wg_level_from = QLineEdit(maxLength=2)

        wg_checkbox_intervals = QCheckBox("To Level")

        wg_level_to = QLineEdit(maxLength=2)
        wg_level_to.setEnabled(False)

        layout_MainSettings.addWidget(wg_modetext)
        layout_MainSettings.addWidget(wg_mode)
        layout_MainSettings.addWidget(wg_leveltext)
        layout_MainSettings.addWidget(wg_level_from)
        layout_MainSettings.addWidget(wg_checkbox_intervals)
        layout_MainSettings.addWidget(wg_level_to)

        # =================
        # Sub: Secondary Settings
        layout_SecSettings = QHBoxLayout()

        wg_cardsperdrawtext = QLabel("# of Songs")
        wg_cardsperdrawtext.setAlignment(Qt.AlignRight)

        wg_numberofcards = QComboBox()
        wg_numberofcards.addItems(["1", "2", "3", "4"])

        wg_songtypestext = QLabel("Song Types")
        wg_arcade_checkbox = QCheckBox("Arcade")
        wg_shortcut_checkbox = QCheckBox("Shorcut")
        wg_fullsong_checkbox = QCheckBox("Full Song")
        wg_remix_checkbox = QCheckBox("Remix")

        layout_SecSettings.addWidget(wg_cardsperdrawtext)
        layout_SecSettings.addWidget(wg_numberofcards)
        layout_SecSettings.addWidget(wg_songtypestext)
        layout_SecSettings.addWidget(wg_arcade_checkbox)
        layout_SecSettings.addWidget(wg_shortcut_checkbox)
        layout_SecSettings.addWidget(wg_fullsong_checkbox)
        layout_SecSettings.addWidget(wg_remix_checkbox)

        # =================

        # Sub: Randomize button
        layout_button = QHBoxLayout()

        wg_button = QPushButton("Randomize!")

        wg_button.clicked.connect(randomize_button)

        layout_button.addWidget(wg_button)

        # =================

        #  Add all to main layout
        main_layout.addLayout(layout_songart)
        main_layout.addLayout(layout_MainSettings)
        main_layout.addLayout(layout_SecSettings)
        main_layout.addLayout(layout_button)
        main_layout.addLayout(layout_cache)

        self.setLayout(main_layout)

    def cacheReload_yes_no(self):

        answer = QMessageBox.question(
            self, "Reload Song Cards cache", cacheText["ReloadCache"])

        if answer != QMessageBox.Yes:
            return

        get_charts_info(chart_type="Single")
        get_charts_info(chart_type="Double")

        cache_dialog = CacheDialog()

        test_json_file = Path("api/dump_Single.json")

        cache_worker = CacheWorker(test_json_file)
        cache_thread = QThread()

        cache_worker.moveToThread(cache_thread)

        # Connections

        cache_dialog.cancel_button.clicked.connect(cache_worker.cancel)

        cache_thread.started.connect(cache_worker.run)

        cache_worker.progress.connect(cache_dialog.progress.setValue)
        cache_worker.status.connect(
            lambda current, total:
            cache_dialog.label.setText(f"Downloaded {current} / {total} songs"
                                       )
        )

        cache_worker.finished.connect(cache_dialog.accept)
        cache_worker.finished.connect(cache_thread.quit)
        cache_worker.finished.connect(cache_worker.deleteLater)
        cache_thread.finished.connect(cache_thread.deleteLater)

        cache_worker.canceled.connect(cache_dialog.reject)

        cache_thread.start()

        print("Downloading...")
        cache_dialog.exec()
        print("Finish download")

    def cacheDelete_yes_no(self):
        if QMessageBox.question(self, "Delete Song Cards cache", cacheText["DeleteCache"]) == QMessageBox.Yes:

            print("Deleting")
            delete_cache()
            print("Finish deleting")

        else:
            return

    def update_cacheProgressBar(self, value):
        self.cacheProgressBar.setValue(value)


class CacheDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.label = QLabel("Downloading cache..")
        self.progress = QProgressBar()
        self.cancel_button = QPushButton("Cancel")

        layout_cachedialog = QVBoxLayout(self)
        layout_cachedialog.addWidget(self.label)
        layout_cachedialog.addWidget(self.progress)
        layout_cachedialog.addWidget(self.cancel_button)
