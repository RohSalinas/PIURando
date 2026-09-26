from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QCheckBox, QMessageBox, QProgressBar, QDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread

from api.api_functions import RandomizerButton
from api.api_maincall import delete_cache, get_charts_info, CacheWorker

from GUI.texts import cacheText
from pathlib import Path


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # =========================
        # Windows size
        # =========================
        self.resize(640, 320)

        # =========================
        # Menu bar
        # =========================
        self.setWindowTitle("Pump it Up - Song Randomizer")
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")

        # =========================
        # Cache Sub Menu
        # =========================
        self.cache_flag = Path("api/appcache/songcards/.cache")
        self.json_singledump = Path("api/appcache/dump_Single.json")
        self.json_doubledump = Path("api/appcache/dump_Double.json")

        layout_cache = QHBoxLayout()

        cacheSubMenu = fileMenu.addMenu("Cache")
        cacheReloadCache = cacheSubMenu.addAction("Reload Song Cards Cache")
        cacheDeleteCache = cacheSubMenu.addAction("Delete Song Cards Cache")

        self.cacheProgressBar = QProgressBar()
        self.cacheProgressBar.setRange(0, 100)

        layout_cache.addWidget(self.cacheProgressBar)

        # =========================
        # Exit, Help and About section
        # =========================
        exitAction = fileMenu.addAction("Exit")

        helpMenu = menubar.addMenu("Help")
        aboutAction = helpMenu.addAction("About")

        # *************************
        # Menu Triggers
        # *************************
        exitAction.triggered.connect(self.close)
        aboutAction.triggered.connect(lambda: QMessageBox.information(self,
                                                                      "About Pump it Up Randomizer",
                                                                      "Work in progress by RoHiSakk"))

        cacheReloadCache.triggered.connect(self.cacheReload_yes_no)
        cacheDeleteCache.triggered.connect(self.cacheDelete_yes_no)

        # =========================
        # Central widget and main layout
        # =========================
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # =========================
        # Song card art section
        # =========================

        layout_songart = QGridLayout()

        wg_songart = QLabel(self)
        pixmap = QPixmap("placeholder.png")
        wg_songart.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        wg_songart.setAlignment(Qt.AlignCenter)

        layout_songart.addWidget(wg_songart, 0, 0)

        # =========================
        # Main settings: Mode, Levels
        # =========================

        layout_MainSettings = QHBoxLayout()

        wg_modetext = QLabel("Mode")

        self.wg_mode = QComboBox()
        self.wg_mode.addItems(["Single", "Double", "Co-Op"])

        self.wg_leveltext = QLabel("From Level")

        self.wg_level_from = QLineEdit(maxLength=2)

        self.wg_checkbox_intervals = QCheckBox("To Level")

        self.wg_level_to = QLineEdit(maxLength=2)
        self.wg_level_to.setEnabled(False)

        layout_MainSettings.addWidget(wg_modetext)
        layout_MainSettings.addWidget(self.wg_mode)
        layout_MainSettings.addWidget(self.wg_leveltext)
        layout_MainSettings.addWidget(self.wg_level_from)
        layout_MainSettings.addWidget(self.wg_checkbox_intervals)
        layout_MainSettings.addWidget(self.wg_level_to)

        # *************************
        # Main Settings Triggers
        # *************************

        self.wg_checkbox_intervals.checkStateChanged.connect(
            self.activate_maxlevel)

        # =========================
        # Sub settings: Song category, number of cards
        # =========================

        layout_SecSettings = QHBoxLayout()

        self.wg_cardsperdrawtext = QLabel("# of Songs")
        self.wg_cardsperdrawtext.setAlignment(Qt.AlignRight)

        self.wg_numberofcards = QComboBox()
        self.wg_numberofcards.addItems(["1", "2", "3", "4"])

        self.wg_songtypestext = QLabel("Song Types")
        self.wg_arcade_checkbox = QCheckBox("Arcade")
        self.wg_shortcut_checkbox = QCheckBox("Shorcut")
        self.wg_fullsong_checkbox = QCheckBox("Full Song")
        self.wg_remix_checkbox = QCheckBox("Remix")

        layout_SecSettings.addWidget(self.wg_cardsperdrawtext)
        layout_SecSettings.addWidget(self.wg_numberofcards)
        layout_SecSettings.addWidget(self.wg_songtypestext)
        layout_SecSettings.addWidget(self.wg_arcade_checkbox)
        layout_SecSettings.addWidget(self.wg_shortcut_checkbox)
        layout_SecSettings.addWidget(self.wg_fullsong_checkbox)
        layout_SecSettings.addWidget(self.wg_remix_checkbox)

        # =========================
        # Randomize button execution
        # =========================
        layout_button = QHBoxLayout()
        randomizer = RandomizerButton()

        wg_button = QPushButton("Randomize!")

        layout_button.addWidget(wg_button)

        wg_button.clicked.connect(lambda: randomizer.randomize_button(self.json_singledump,
                                                                      self.json_doubledump,
                                                                      self.wg_mode.currentText(),
                                                                      self.wg_level_from.text(),
                                                                      self.wg_level_to.text(),
                                                                      self.wg_numberofcards.currentText(
                                                                      ),
                                                                      {
                                                                          "arcade": self.wg_arcade_checkbox.isChecked(),
                                                                          "shortcut": self.wg_shortcut_checkbox.isChecked(),
                                                                          "fullsong": self.wg_fullsong_checkbox.isChecked(),
                                                                          "remix": self.wg_remix_checkbox.isChecked()
                                                                      },
                                                                      self.wg_checkbox_intervals.isChecked()))

        randomizer.error_nominlvl.connect(lambda: QMessageBox.information(self,
                                                                          "Minimum level missing",
                                                                          "Please input a minimum song level for your search"))
        randomizer.error_minovermax.connect(lambda: QMessageBox.information(self,
                                                                            "Max level too low",
                                                                            "Your 'Max level' cannot be lower than your 'Min level'"))
        # =========================
        # Add all layouts to Main Layout
        # =========================
        main_layout.addLayout(layout_songart)
        main_layout.addLayout(layout_MainSettings)
        main_layout.addLayout(layout_SecSettings)
        main_layout.addLayout(layout_button)
        main_layout.addLayout(layout_cache)

        self.setLayout(main_layout)
        self.first_time_cache()

        # =========================
        # Cache Files location
        # =========================
        self.cache_flag = Path("api/appcache/songcards/.cache")
        self.json_singledump = Path("api/appcache/dump_Single.json")
        self.json_doubledump = Path("api/appcache/dump_Double.json")

# ==========================================================================================================================================================

    def first_time_cache(self):
        if not self.cache_flag.exists():
            self.cache_flag = QMessageBox.question(
                self, "No Cache found", cacheText["FirstTime"])

        if self.cache_flag != QMessageBox.Yes:
            return
        else:
            get_charts_info(chart_type="Single")
            get_charts_info(chart_type="Double")
            jsondump_forsongcard = Path("api/appcache/dump_Single.json")

            # Keep references alive
            self.cache_dialog = CacheDialog(self)
            self.cache_thread = QThread()
            self.cache_worker = CacheWorker(jsondump_forsongcard)
            self.cache_worker.moveToThread(self.cache_thread)

            self.cache_thread.started.connect(self.cache_worker.run)

            self.cache_worker.progress.connect(
                self.cache_dialog.progress.setValue)
            self.cache_worker.status.connect(
                lambda current, total:
                self.cache_dialog.label.setText(
                    f"Downloaded {current} / {total} songs")
            )

            self.cache_worker.finished.connect(self.cache_dialog.accept)

            # Cleanup
            self.cache_worker.finished.connect(self.cache_thread.quit)

            self.cache_thread.finished.connect(self.cache_worker.deleteLater)
            self.cache_thread.finished.connect(self.cache_thread.deleteLater)

            # Start
            self.cache_thread.start()
            self.cache_dialog.exec()

            # Finish
            if self.cache_dialog.finished:
                self.cache_confirmation = QMessageBox.information(
                    self, "First Cache", "Song cards downloaded successfully!")

    def cacheReload_yes_no(self):
        cache_answer = QMessageBox.question(
            self, "Reload Song Cards cache", cacheText["ReloadCache"])

        if cache_answer != QMessageBox.Yes:
            return

        get_charts_info(chart_type="Single")
        get_charts_info(chart_type="Double")
        jsondump_forsongcard = Path("api/dump_Single.json")

        # Keep references alive
        self.cache_dialog = CacheDialog(self)
        self.cache_thread = QThread()
        self.cache_worker = CacheWorker(jsondump_forsongcard)
        self.cache_worker.moveToThread(self.cache_thread)

        self.cache_thread.started.connect(self.cache_worker.run)

        self.cache_worker.progress.connect(self.cache_dialog.progress.setValue)
        self.cache_worker.status.connect(
            lambda current, total:
            self.cache_dialog.label.setText(
                f"Downloaded {current} / {total} songs")
        )

        self.cache_worker.finished.connect(self.cache_dialog.accept)

        # Cleanup
        self.cache_worker.finished.connect(self.cache_thread.quit)

        self.cache_thread.finished.connect(self.cache_worker.deleteLater)
        self.cache_thread.finished.connect(self.cache_thread.deleteLater)

        # Start
        self.cache_thread.start()
        self.cache_dialog.exec()

        # Finish
        if self.cache_dialog.finished:
            self.cache_confirmation = QMessageBox.information(
                self, "Reload Cache", "Song cards updated successfully!")

    def cacheDelete_yes_no(self):

        if QMessageBox.question(self, "Delete Song Cards cache", cacheText["DeleteCache"]) == QMessageBox.Yes:

            print("Deleting")
            delete_cache()
            print("Finish deleting")
            self.cache_confirmation = QMessageBox.information(
                self, "Reload Cache", "Song cards updated successfully!")

        else:
            return

    def update_cacheProgressBar(self, value):
        self.cacheProgressBar.setValue(value)

    def activate_maxlevel(self):
        checkflag = self.wg_checkbox_intervals.isChecked()
        if checkflag:
            self.wg_level_to.setEnabled(True)
        else:
            self.wg_level_to.setEnabled(False)
            self.wg_level_to.clear()

# ==========================================================================================================================================================


class CacheDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Downloading Cache")
        self.label = QLabel("Downloading cache..")
        self.progress = QProgressBar()

        layout_cachedialog = QVBoxLayout(self)
        layout_cachedialog.addWidget(self.label)
        layout_cachedialog.addWidget(self.progress)
