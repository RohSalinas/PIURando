from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QCheckBox, QMessageBox, QProgressBar, QDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread

from api.api_functions import RandomizerButton
from api.api_maincall import delete_cache, get_charts_info, CacheWorker

from GUI.texts import cacheText, stylesheets
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
        self.json_dump = Path("api/appcache/dump_all.json")

        layout_cache = QHBoxLayout()

        cacheSubMenu = fileMenu.addMenu("Cache")
        cacheReloadCache = cacheSubMenu.addAction("Reload song cards cache")
        cacheDeleteCache = cacheSubMenu.addAction("Delete song cards cache")

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

        self.randomizer = RandomizerButton()

        # =========================
        # Song Card Art section
        # =========================

        layout_songart = QGridLayout()

        self.wg_songart = ImageLabel()
        self.wg_songart.set_image("placeholder.png")
        self.wg_songart.setAlignment(Qt.AlignCenter)

        layout_songart.addWidget(self.wg_songart, 0, 0)

        # *************************
        # Song Card Art Triggers
        # *************************

        # self.randomizer = RandomizerButton()
        self.randomizer.randomize_over.connect(
            self.randomizer.assign_chart_to_image)
        self.randomizer.imagechange.connect(
            lambda path: self.wg_songart.set_image(path)
        )
        # self.randomizer.imagechange.connect(
        #     lambda path: self.wg_songart.setPixmap(QPixmap(path))
        # )

        # =========================
        # Song Level
        # =========================

        layout_ShowLevel = QHBoxLayout()

        self.wg_showlevel = QLabel("Selected chart level will be shown here.")
        self.wg_showlevel.setAlignment(Qt.AlignCenter)
        self.wg_showlevel.setFixedHeight(50)

        self.wg_showlevel.setStyleSheet(stylesheets["defaultLevel"])

        layout_ShowLevel.addWidget(self.wg_showlevel)

        # *************************
        # Song Level Triggers
        # *************************

        self.randomizer.levelchange.connect(
            lambda level: self.wg_showlevel.setText(level))
        self.randomizer.levelchange.connect(lambda level:
                                            self.wg_showlevel.setStyleSheet(stylesheets["greenStyle"]) if "D" in level else
                                            self.wg_showlevel.setStyleSheet(stylesheets["redStyle"]) if "S" in level else
                                            self.wg_showlevel.setStyleSheet(stylesheets["coopStyle"]))

        # =========================
        # Main settings: Mode, Levels
        # =========================

        layout_MainSettings = QHBoxLayout()

        wg_modetext = QLabel("Mode")

        self.wg_mode = QComboBox()
        self.wg_mode.addItems(["Single", "Double", "Co-Op"])

        self.wg_coop_text = QLabel("Co-Op players")
        self.wg_coop_players = QComboBox()
        self.wg_coop_players.addItems(["any", "2", "3", "4", "5"])
        self.wg_coop_players.setEnabled(False)

        self.wg_leveltext = QLabel("From Level")

        self.wg_level_from = QLineEdit(maxLength=2)

        self.wg_checkbox_intervals = QCheckBox("To Level")

        self.wg_level_to = QLineEdit(maxLength=2)
        self.wg_level_to.setEnabled(False)

        layout_MainSettings.addWidget(wg_modetext)
        layout_MainSettings.addWidget(self.wg_mode)
        layout_MainSettings.addWidget(self.wg_coop_text)
        layout_MainSettings.addWidget(self.wg_coop_players)
        layout_MainSettings.addWidget(self.wg_leveltext)
        layout_MainSettings.addWidget(self.wg_level_from)
        layout_MainSettings.addWidget(self.wg_checkbox_intervals)
        layout_MainSettings.addWidget(self.wg_level_to)

        # *************************
        # Main Settings Triggers
        # *************************

        self.wg_checkbox_intervals.checkStateChanged.connect(
            self.activate_maxlevel)
        self.wg_mode.currentTextChanged.connect(self.activate_coop_players)

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

        self.wg_offlinemode_text = QLabel("Offline mode")
        self.wg_offlinemode_text.setStyleSheet("""
            QLabel {
                color: white;
                background-color: navyblue;
                font-weight: bold;
                border-radius:5px;
            }
            """)
        self.wg_offlinemode = QCheckBox()

        layout_SecSettings.addWidget(self.wg_cardsperdrawtext)
        layout_SecSettings.addWidget(self.wg_numberofcards)
        layout_SecSettings.addWidget(self.wg_songtypestext)
        layout_SecSettings.addWidget(self.wg_arcade_checkbox)
        layout_SecSettings.addWidget(self.wg_shortcut_checkbox)
        layout_SecSettings.addWidget(self.wg_fullsong_checkbox)
        layout_SecSettings.addWidget(self.wg_remix_checkbox)
        layout_SecSettings.addWidget(self.wg_offlinemode_text)
        layout_SecSettings.addWidget(self.wg_offlinemode)

        # *************************
        # Sub Settings Triggers
        # *************************

        self.wg_offlinemode.toggled.connect(
            self.check_change_internet)

        # =========================
        # Randomize button execution
        # =========================
        layout_button = QHBoxLayout()
        # randomizer = RandomizerButton()

        wg_button = QPushButton("Randomize!")

        layout_button.addWidget(wg_button)

        wg_button.clicked.connect(lambda: self.randomizer.randomize_button(self.json_dump,
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
                                                                           self.wg_coop_players.currentText(),
                                                                           self.wg_checkbox_intervals.isChecked(),
                                                                           offlinemode=self.wg_offlinemode.isChecked()
                                                                           )
                                  )

        self.randomizer.error_nominlvl.connect(lambda: QMessageBox.information(self,
                                                                               "Minimum level missing",
                                                                               "Please input a minimum song level for your search"))
        self.randomizer.error_minovermax.connect(lambda: QMessageBox.information(self,
                                                                                 "Max level too low",
                                                                                 "Your 'Max level' cannot be lower than your 'Min level'"))
        self.randomizer.error_nolevel.connect(lambda: QMessageBox.information(self,
                                                                              "Chart not found",
                                                                              "No charts were found. Please try different value(s) and/or filters."))

        # =========================
        # Add all layouts to Main Layout
        # =========================
        main_layout.addLayout(layout_songart)
        main_layout.addLayout(layout_ShowLevel)
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
        self.json_dump = Path("api/appcache/dump_all.json")

# ==========================================================================================================================================================
# ==========================================================================================================================================================
# ==========================================================================================================================================================
# ==========================================================================================================================================================
# ==========================================================================================================================================================

    def first_time_cache(self):
        if self.cache_flag.exists():
            self.wg_offlinemode.setChecked(True)
            return

        if not self.cache_flag.exists():
            self.cache_flag = QMessageBox.question(
                self, "No Cache found", cacheText["FirstTime"])

        if self.cache_flag != QMessageBox.Yes:
            return
        else:
            get_charts_info(chart_type="Single")
            get_charts_info(chart_type="Double")
            get_charts_info()
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
                self.wg_offlinemode.setChecked(True)
                self.cache_confirmation = QMessageBox.information(
                    self, "First Cache", "Song cards downloaded successfully!")

    def cacheReload_yes_no(self):
        cache_answer = QMessageBox.question(
            self, "Reload Song Cards cache", cacheText["ReloadCache"])

        if cache_answer != QMessageBox.Yes:
            return

        get_charts_info(chart_type="Single")
        get_charts_info(chart_type="Double")
        get_charts_info()
        jsondump_forsongcard = Path("api/appcache/dump_Single.json")

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
            self.wg_offlinemode.setChecked(True)
            self.rel_cache_confirmation = QMessageBox.information(
                self, "Reload Cache", "Song cards updated successfully!")

    def cacheDelete_yes_no(self):

        if QMessageBox.question(self, "Delete Song Cards cache", cacheText["DeleteCache"]) == QMessageBox.Yes:

            print("Deleting")
            delete_cache()
            print("Finish deleting")
            self.def_cache_confirmation = QMessageBox.information(
                self, "Delete Cache", "Song cards cache deleted successfully!")

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

    def activate_coop_players(self):
        checkflag = self.wg_mode.currentText()
        if checkflag == "Co-Op":
            self.wg_coop_players.setEnabled(True)
            self.wg_numberofcards.setEnabled(False)
        else:
            self.wg_coop_players.setEnabled(False)
            self.wg_numberofcards.setEnabled(True)

    def check_change_internet(self, checked):
        if checked:
            if self.cache_flag.exists():
                return

            self.online_cof = QMessageBox.information(
                self, "Internet Mode", cacheText["On_to_OfflineMode_nocache"])
            self.wg_offlinemode.blockSignals(True)
            self.wg_offlinemode.setChecked(False)
            self.wg_offlinemode.blockSignals(False)

        else:
            if self.cache_flag.exists():
                self.online_cof = QMessageBox.information(
                    self, "Internet Mode", cacheText["Off_to_OnlineMode_cache"])
            else:
                self.online_cof = QMessageBox.information(
                    self, "Internet Mode", cacheText["Off_to_OnlineMode_nocache"])
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


class ImageLabel(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap_original = QPixmap()

    def set_image(self, path):
        self.pixmap_original = QPixmap(path)
        self.update_image()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image()

    def update_image(self):
        if self.pixmap_original.isNull():
            return

        scaled = self.pixmap_original.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.setPixmap(scaled)
