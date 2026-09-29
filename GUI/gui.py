from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QLabel, QSizePolicy
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
        self.resize(1280, 640)

        # =========================
        # Menu bar
        # =========================
        self.setWindowTitle("Pump it Up - Song Chart Randomizer")
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")

        # =========================
        # Cache Sub Menu
        # =========================
        self.cache_flag = Path("api/appcache/songcards/.cache")
        self.json_dump = Path("api/appcache/dump_all.json")

        # layout_cache = QHBoxLayout()

        cacheSubMenu = fileMenu.addMenu("Cache")
        cacheReloadCache = cacheSubMenu.addAction("Reload song cards cache")
        cacheDeleteCache = cacheSubMenu.addAction("Delete song cards cache")

        self.cacheProgressBar = QProgressBar()
        self.cacheProgressBar.setRange(0, 100)

        # layout_cache.addWidget(self.cacheProgressBar)

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
        # Song Card Art / Level section
        # =========================

        self.layout_songart = QGridLayout()

        self.layout_songart.setContentsMargins(10, 10, 10, 10)
        self.layout_songart.setSpacing(10)

        # Make both columns equal width
        self.layout_songart.setColumnStretch(0, 1)
        self.layout_songart.setColumnStretch(1, 1)

        self.song_images = []
        self.song_levels = []

        for i in range(4):

            image = ImageLabel()

            level = QLabel("")
            level.setAlignment(Qt.AlignCenter)
            level.setFixedHeight(50)
            level.setStyleSheet(stylesheets["defaultLevel"])

            self.song_images.append(image)
            self.song_levels.append(level)

        for i in range(4):

            row = i // 2
            col = i % 2

            self.layout_songart.addWidget(self.song_images[i], row * 2, col)
            self.layout_songart.addWidget(
                self.song_levels[i], row * 2 + 1, col)

        self.layout_songart.setColumnStretch(0, 1)
        self.layout_songart.setColumnStretch(1, 0)

        self.song_images[0].set_image("cover.png")
        self.song_images[0].show()

        self.song_levels[0].setText(
            "Choose your settings and press 'Randomize' to start!")
        self.song_levels[0].show()

        for image in self.song_images[1:]:
            image.hide()

        for level in self.song_levels[1:]:
            level.hide()

        # *************************
        # Song Card Art /Level Triggers
        # *************************

        self.randomizer.randomize_over.connect(
            self.randomizer.assign_chart_to_image)

        self.randomizer.newcharts_ok.connect(self.update_song_cards)

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
        wg_button.setStyleSheet(stylesheets["randomize"])

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
        main_layout.addLayout(self.layout_songart)
        main_layout.addLayout(layout_MainSettings)
        main_layout.addLayout(layout_SecSettings)
        main_layout.addLayout(layout_button)
        # main_layout.addLayout(layout_cache)

        self.setLayout(main_layout)
        self.first_time_cache()

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
            # self.wg_numberofcards.set
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

    def update_song_cards(self, charts):

        # Remove widgets from the layout (Fresh start)
        for image in self.song_images:
            self.layout_songart.removeWidget(image)

        for level in self.song_levels:
            self.layout_songart.removeWidget(level)

        # Hide everything (Fresh start)
        for image in self.song_images:
            image.hide()

        for level in self.song_levels:
            level.hide()

        if len(charts) == 1:
            self.layout_songart.setColumnStretch(0, 1)
            self.layout_songart.setColumnStretch(1, 0)

            image = self.song_images[0]
            level = self.song_levels[0]

            image.set_image(charts[0]["image"])
            level.setText(charts[0]["level"])

            self.set_level_style(level, charts[0]["level"])

            self.layout_songart.addWidget(image, 0, 0, 1, 2)
            self.layout_songart.addWidget(level, 1, 0, 1, 2)

            image.show()
            level.show()

        else:

            self.layout_songart.setColumnStretch(0, 1)
            self.layout_songart.setColumnStretch(1, 1)

            for i, chart in enumerate(charts):

                image = self.song_images[i]
                level = self.song_levels[i]

                image.set_image(chart["image"])
                level.setText(chart["level"])

                self.set_level_style(level, chart["level"])

                row = i // 2
                col = i % 2

                self.layout_songart.addWidget(image, row * 2, col)
                self.layout_songart.addWidget(level, row * 2 + 1, col)

                image.show()
                level.show()

    def set_level_style(self, label, level):

        if "D" in level:
            label.setStyleSheet(stylesheets["greenStyle"])

        elif "S" in level:
            label.setStyleSheet(stylesheets["redStyle"])

        elif "C" in level:
            label.setStyleSheet(stylesheets["coopStyle"])

        else:
            label.setStyleSheet(stylesheets["defaultLevel"])

# ==============================================================================================================================================
# ==============================================================================================================================================
# ==============================================================================================================================================
# ==============================================================================================================================================
# ==============================================================================================================================================


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

        self.setAlignment(Qt.AlignCenter)

        # Allow the layout to freely resize the label
        self.setMinimumSize(0, 0)
        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

    def set_image(self, path):
        self.pixmap_original = QPixmap(str(path))
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
        self.setAlignment(Qt.AlignCenter)

    # Important: don't let the original image dictate
    # the minimum size of the window.
    def sizeHint(self):
        return QSize(0, 0)

    def minimumSizeHint(self):
        return QSize(0, 0)
