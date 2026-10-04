from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QLabel, QSizePolicy, QApplication
from PySide6.QtWidgets import QMainWindow, QLabel, QFrame, QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QCheckBox, QMessageBox, QProgressBar, QDialog, QFormLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread

from api.api_functions import RandomizerButton
from api.api_maincall import delete_cache, CacheWorker, get_charts_info_v2

from GUI.texts import cacheText, stylesheets, menuText
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
        self.json_dump = Path("api/appcache/dump_all_v2.json")
        self.token = Path("api/appcache/token.txt")

        cacheSubMenu = fileMenu.addMenu("Cache")
        cacheReloadCache = cacheSubMenu.addAction("Reload song cards cache")
        cacheDeleteCache = cacheSubMenu.addAction("Delete song cards cache")

        self.cacheProgressBar = QProgressBar()
        self.cacheProgressBar.setRange(0, 100)

        # =========================
        # User section
        # =========================

        userMenu = menubar.addMenu("User")
        APISubMenu = userMenu.addAction("API Key Configuration")

        self.API_dialog = APITokenWindow(self)

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

        APISubMenu.triggered.connect(self.API_dialog.exec)
# ==========================================================================================================================================================
        # =========================
        # Central widget and main layout
        # =========================
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QGridLayout(central_widget)
        main_layout.setColumnStretch(0, 0.2)
        main_layout.setColumnStretch(1, 3)

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

        for i in range(6):

            image = ImageLabel()

            level = QLabel("")
            level.setAlignment(Qt.AlignCenter)
            level.setFixedHeight(50)
            level.setStyleSheet(stylesheets["defaultLevel"])

            self.song_images.append(image)
            self.song_levels.append(level)

        for i in range(6):

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

# ==========================================================================================================================================================
        # =========================
        # Main settings: Mode, Levels
        # =========================
        layout_MainSettings = QVBoxLayout()
        layout_MainSettings.setAlignment(Qt.AlignTop)

        self.separator1 = QFrame()
        self.separator1.setFrameShape(QFrame.HLine)
        self.separator1.setFrameShadow(QFrame.Sunken)

        layout_MainH1 = QHBoxLayout()
        layout_MainH2 = QHBoxLayout()

        wg_mainsettingstitle = QLabel("Customize Settings")
        wg_mainsettingstitle.setFixedHeight(50)
        wg_mainsettingstitle.setStyleSheet(stylesheets["MainSettings"])
        wg_mainsettingstitle.setAlignment(Qt.AlignCenter)

        wg_modetext = QLabel("Step Type")
        wg_modetext.setAlignment(Qt.AlignLeft)

        self.wg_mode = QComboBox()
        self.wg_mode.setFixedWidth(200)
        self.wg_mode.addItems(["Single", "Double", "Co-Op"])

        self.wg_coop_text = QLabel("# Co-Op players")
        self.wg_coop_players = QComboBox()
        self.wg_coop_players.addItems(["any", "2", "3", "4", "5"])
        self.wg_coop_players.setEnabled(False)

        self.wg_leveltext = QLabel("Min Level")
        self.wg_level_from = QLineEdit(maxLength=2)
        self.wg_level_from.setFixedWidth(45)
        self.wg_checkbox_intervals = QCheckBox("Max Level")
        self.wg_level_to = QLineEdit(maxLength=2)
        self.wg_level_to.setFixedWidth(45)
        self.wg_level_to.setEnabled(False)

        self.wg_cardsperdrawtext = QLabel("Number of\nRandom Songs")
        self.wg_cardsperdrawtext.setAlignment(Qt.AlignRight)

        self.wg_numberofcards = QComboBox()
        self.wg_numberofcards.addItems(["1", "2", "3", "4", "5", "6"])

        layout_MainH1.addWidget(wg_modetext)
        layout_MainH1.addWidget(self.wg_mode)
        layout_MainH1.addWidget(self.wg_coop_text)
        layout_MainH1.addWidget(self.wg_coop_players)

        layout_MainH2.addWidget(self.wg_leveltext)
        layout_MainH2.addWidget(self.wg_level_from)
        layout_MainH2.addWidget(self.wg_checkbox_intervals)
        layout_MainH2.addWidget(self.wg_level_to)

        layout_MainH2.addWidget(self.wg_cardsperdrawtext)
        layout_MainH2.addWidget(self.wg_numberofcards)

        layout_MainSettings.addWidget(wg_mainsettingstitle)
        layout_MainSettings.addWidget(self.separator1)
        layout_MainSettings.addLayout(layout_MainH1)
        layout_MainSettings.addLayout(layout_MainH2)

        # *************************
        # Main Settings Triggers
        # *************************

        self.wg_checkbox_intervals.checkStateChanged.connect(
            lambda state: self.activate_maxlevel(
                state, self.wg_level_to))

        self.wg_mode.currentTextChanged.connect(self.activate_coop_players)

# ==========================================================================================================================================================
        # =========================
        # Sub settings: Song category, number of cards
        # =========================
        layout_SecSettingsV = QVBoxLayout()
        layout_SecSettingsH1 = QHBoxLayout()
        layout_SecSettingsH2 = QHBoxLayout()

        # layout_SecSettingsH1.setAlignment(Qt.AlignTop)

        self.wg_secsettingstitle = QLabel("Extra Filters")
        self.wg_secsettingstitle.setStyleSheet(stylesheets["SecSettings"])
        self.wg_secsettingstitle.setAlignment(Qt.AlignCenter)
        self.wg_secsettingstitle.setFixedHeight(35)

        self.wg_songtypestext = QLabel("Song Types")
        self.wg_arcade_checkbox = QCheckBox("Arcade")
        self.wg_shortcut_checkbox = QCheckBox("Shorcut")
        self.wg_fullsong_checkbox = QCheckBox("Full Song")
        self.wg_remix_checkbox = QCheckBox("Remix")

        self.wg_reset_button = QPushButton("Reset to default")
        self.wg_reset_button.clicked.connect(self.reset_defaults)

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

        self.separator2 = QFrame()
        self.separator2.setFrameShape(QFrame.HLine)
        self.separator2.setFrameShadow(QFrame.Sunken)

        layout_SecSettingsH1.addWidget(self.wg_songtypestext)
        layout_SecSettingsH1.addWidget(self.wg_arcade_checkbox)
        layout_SecSettingsH1.addWidget(self.wg_shortcut_checkbox)
        layout_SecSettingsH1.addWidget(self.wg_fullsong_checkbox)
        layout_SecSettingsH1.addWidget(self.wg_remix_checkbox)

        layout_SecSettingsH2.addWidget(self.wg_reset_button)
        layout_SecSettingsH2.addWidget(self.wg_offlinemode_text)
        layout_SecSettingsH2.addWidget(self.wg_offlinemode)
        layout_SecSettingsH2.setAlignment(Qt.AlignCenter)

        layout_SecSettingsV.addWidget(self.wg_secsettingstitle)
        layout_SecSettingsV.addWidget(self.separator2)
        layout_SecSettingsV.addLayout(layout_SecSettingsH1)
        layout_SecSettingsV.addLayout(layout_SecSettingsH2)

        # *************************
        # Sub Settings Triggers
        # *************************

        self.wg_offlinemode.toggled.connect(
            self.check_change_internet)
# ==========================================================================================================================================================
        # =========================
        # Predefined Settings:
        # =========================
        # ComboBox with options:
        # =========================

        layout_pred_setting = QVBoxLayout()
        self.layout_pred_settingH1 = QHBoxLayout()
        self.layout_pred_settingH1.setAlignment(Qt.AlignCenter)

        self.wg_pred_settings_title = QLabel("Predefined Settings")
        self.wg_pred_settings_title.setStyleSheet(stylesheets["SecSettings"])
        self.wg_pred_settings_title.setAlignment(Qt.AlignCenter)
        self.wg_pred_settings_title.setFixedHeight(35)

        self.activate_predetermined_checkbox = QCheckBox()

        self.predetermined_settings_combobox = QComboBox()
        self.predetermined_settings_combobox.addItems([
            menuText["Settings1"],
            menuText["Settings2"],
            menuText["Settings3"],
            menuText["Settings4"],
            menuText["Settings5"],
            menuText["Settings6"]
        ])
        self.predetermined_settings_combobox.setEnabled(False)

        self.layout_pred_settingH1.addWidget(
            self.activate_predetermined_checkbox)
        self.layout_pred_settingH1.addWidget(
            self.predetermined_settings_combobox)

        layout_pred_setting.addWidget(self.wg_pred_settings_title)
        layout_pred_setting.addLayout(self.layout_pred_settingH1)

        # =========================
        # Predefined widgets:
        # =========================
        self.predefined_rows = []

        for i in range(6):
            self.layout_pf = QHBoxLayout()

            self.pf_row_active = QCheckBox()
            self.pf_row_active.setEnabled(False)

            self.pf_steptype_text = QLabel("Step Type")
            self.pf_steptype = QComboBox()
            self.pf_steptype.addItems(["Single", "Double"])
            self.pf_steptype.setEnabled(False)

            self.pf_minleveltext = QLabel("Min Level")
            self.pf_minlevel = QLineEdit(maxLength=2)
            self.pf_minlevel.setFixedWidth(45)
            self.pf_minlevel.setEnabled(False)

            self.pf_checkbox = QCheckBox("Max Level")
            self.pf_checkbox.setEnabled(False)

            self.pf_maxlevel = QLineEdit(maxLength=2)
            self.pf_maxlevel.setFixedWidth(45)
            self.pf_maxlevel.setEnabled(False)

            self.pf_checkbox.checkStateChanged.connect(
                lambda state, maxlevel=self.pf_maxlevel: self.activate_maxlevel(
                    state, maxlevel))

            self.layout_pf.addWidget(self.pf_row_active)
            self.layout_pf.addWidget(self.pf_steptype_text)
            self.layout_pf.addWidget(self.pf_steptype)
            self.layout_pf.addWidget(self.pf_minleveltext)
            self.layout_pf.addWidget(self.pf_minlevel)
            self.layout_pf.addWidget(self.pf_checkbox)
            self.layout_pf.addWidget(self.pf_maxlevel)

            self.predefined_rows.append({
                "active": self.pf_row_active,
                "steptype": self.pf_steptype,
                "layout": self.layout_pf,
                "min": self.pf_minlevel,
                "checkbox": self.pf_checkbox,
                "max": self.pf_maxlevel,
            })
        for i in range(6):
            layout_pred_setting.addLayout(self.predefined_rows[i]["layout"])

        # *************************
        # Predefined Settings Triggers
        # *************************

            self.activate_predetermined_checkbox.checkStateChanged.connect(
                self.activate_pred_settings)

            self.activate_predetermined_checkbox.checkStateChanged.connect(
                self.pred_menu_defaults)

            self.predetermined_settings_combobox.currentTextChanged.connect(
                self.pred_menu_defaults)


# ==========================================================================================================================================================
        # =========================
        # Randomize button execution
        # =========================
        layout_button = QHBoxLayout()
        # randomizer = RandomizerButton()

        wg_button = QPushButton("Randomize!")
        wg_button.setStyleSheet(stylesheets["randomize"])

        layout_button.addWidget(wg_button)

        wg_button.clicked.connect(self.on_randomizer_event)

        self.randomizer.error_nominlvl.connect(lambda: QMessageBox.information(self,
                                                                               "Minimum level missing",
                                                                               "Please input a minimum song level for your search"))

        self.randomizer.error_minovermax.connect(lambda: QMessageBox.information(self,
                                                                                 "Max level too low",
                                                                                 "Your 'Max level' cannot be lower than your 'Min level'"))

        self.randomizer.error_nomaxlevel_whentrue.connect(lambda: QMessageBox.information(self,
                                                                                          "Maxium level missing",
                                                                                          "You have the 'Max Level' filter activated. Please input a maximum song level for your search"))

        self.randomizer.error_nolevel.connect(lambda: QMessageBox.information(self,
                                                                              "Chart not found",
                                                                              "No charts were found. Please try different value(s) and/or filters."))

        self.randomizer.error_notenoughcharts.connect(lambda requested, available: QMessageBox.information(self,
                                                                                                           "Not enough charts",
                                                                                                           f"While you asked for {requested} song cards, your filters give a total of {available} song cards.\n"
                                                                                                           "Please change your maximum number of song cards requested"))

# ==========================================================================================================================================================
        # =========================
        # Add all layouts to Main Layout
        # =========================

        setting_layout = QVBoxLayout()
        setting_layout.addLayout(layout_MainSettings)
        setting_layout.addLayout(layout_SecSettingsV)
        setting_layout.addLayout(layout_pred_setting)

        setting_layout.addStretch()

        setting_layout.addLayout(layout_button)

        main_layout.addLayout(setting_layout, 0, 0)
        main_layout.addLayout(self.layout_songart, 0, 1)

        self.setLayout(main_layout)
        self.first_time_cache()

# ==========================================================================================================================================================
# ==========================================================================================================================================================
# ==========================================================================================================================================================
# ==========================================================================================================================================================
# ==========================================================================================================================================================

    def first_time_cache(self):

        APPCACHE_DIR = Path("api/appcache")
        SONGS_DIR = Path(APPCACHE_DIR / "songcards")

        APPCACHE_DIR.parent.mkdir(parents=True, exist_ok=True)
        SONGS_DIR.mkdir(parents=True, exist_ok=True)

        if self.cache_flag.exists():
            self.wg_offlinemode.setChecked(True)
            return

        if not self.cache_flag.exists():
            cache_answer = QMessageBox.question(
                self, "No Cache found", cacheText["FirstTime"])

        if cache_answer != QMessageBox.Yes:
            return

        else:

            api_flag = self.no_API_key_window()

            if not api_flag:
                QMessageBox.warning(
                    self,
                    "Connection failed",
                    "Could not access the remote server.\n\n"
                    "Please check your API key and try again."
                )
                return

            self.cache_gettingjson = QDialog(self)
            self.cache_gettingjson.setWindowTitle("Reloading songs cache")
            self.cache_gettingjson.setFixedSize(200, 75)

            layout_gettingjson = QVBoxLayout(self.cache_gettingjson)
            label = QLabel("Getting songs metadata...")
            label.setAlignment(Qt.AlignCenter)
            layout_gettingjson.addWidget(label)

            self.cache_gettingjson.show()
            self.cache_gettingjson.raise_()
            self.cache_gettingjson.activateWindow()

            for _ in range(3):
                QApplication.processEvents()
            self.cache_gettingjson.repaint()

            data = get_charts_info_v2(mix="phoenix2")

            self.cache_gettingjson.close()

            if data is None:
                QMessageBox.warning(
                    self,
                    "Connection failed",
                    "Could not access the remote server.\n\n"
                    "Please check your internet connection or API key and try again."
                )
                return

            jsondump_forsongcard = Path("api/appcache/dump_all_v2.json")

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

        if not self.token:
            api_flag = self.no_API_key_window()

            if not api_flag:
                QMessageBox.warning(
                    self,
                    "Connection failed",
                    "Could not access the remote server.\n\n"
                    "Please check your API key and try again."
                )
                return

        self.cache_gettingjson = QDialog(self)
        self.cache_gettingjson.setWindowTitle("Reloading songs cache")
        self.cache_gettingjson.setFixedSize(200, 75)

        layout_gettingjson = QVBoxLayout(self.cache_gettingjson)
        label = QLabel("Getting songs metadata...")
        label.setAlignment(Qt.AlignCenter)
        layout_gettingjson.addWidget(label)

        self.cache_gettingjson.show()
        self.cache_gettingjson.raise_()
        self.cache_gettingjson.activateWindow()

        for _ in range(3):
            QApplication.processEvents()
        self.cache_gettingjson.repaint()

        data = get_charts_info_v2(mix="phoenix2")

        self.cache_gettingjson.close()

        if data is None:
            QMessageBox.warning(
                self,
                "Connection failed",
                "Could not access the remote server.\n\n"
                "Please check your internet connection and try again."
            )
            return

        print("Before json check")
        jsondump_forsongcard = Path("api/appcache/dump_all_v2.json")
        print("After json check")

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
            self.wg_offlinemode.blockSignals(True)
            self.wg_offlinemode.setChecked(True)
            self.wg_offlinemode.blockSignals(False)
            self.rel_cache_confirmation = QMessageBox.information(
                self, "Reload Cache", "Song cards updated successfully!")

    def cacheDelete_yes_no(self):

        if QMessageBox.question(self, "Delete Song Cards cache", cacheText["DeleteCache"]) == QMessageBox.Yes:

            print("Deleting")
            delete_cache(self.API_dialog)
            print("Finish deleting")
            self.def_cache_confirmation = QMessageBox.information(
                self, "Delete Cache", "Song cards cache deleted successfully!")

        else:
            return

    def update_cacheProgressBar(self, value):
        self.cacheProgressBar.setValue(value)

    def activate_maxlevel(self, state, level_wg: QLineEdit):

        if state == Qt.Checked:
            level_wg.setEnabled(True)
        else:
            level_wg.setEnabled(False)
            level_wg.clear()

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

    def no_API_key_window(self):
        self.API_dialog.exec()

        token_path = Path("api/appcache/token.txt")

        if not token_path.exists():
            self.token_not_ok = QMessageBox.information(self,
                                                        "API Token",
                                                        "You haven't input a token. Cache download cannot proceed.")
            return None

        token = token_path.read_text(encoding="utf-8").strip()

        if not token:
            return None

        return token

    def reset_defaults(self):
        self.wg_mode.setCurrentIndex(0)
        self.wg_coop_players.setCurrentIndex(0)
        self.wg_level_from.clear()
        self.wg_level_to.clear()
        self.wg_numberofcards.setCurrentIndex(0)
        self.wg_arcade_checkbox.setChecked(False)
        self.wg_remix_checkbox.setChecked(False)
        self.wg_fullsong_checkbox.setChecked(False)
        self.wg_shortcut_checkbox.setChecked(False)
        self.wg_checkbox_intervals.setChecked(False)

    def deactivate_by_pred(self):
        self.wg_mode.setEnabled(False)
        self.wg_coop_players.setEnabled(False)
        self.wg_level_from.setEnabled(False)
        self.wg_level_to.setEnabled(False)
        self.wg_numberofcards.setEnabled(False)
        self.wg_arcade_checkbox.setEnabled(False)
        self.wg_remix_checkbox.setEnabled(False)
        self.wg_fullsong_checkbox.setEnabled(False)
        self.wg_shortcut_checkbox.setEnabled(False)
        self.wg_checkbox_intervals.setEnabled(False)

    def activate_by_pred(self):
        print("Activating shit")
        self.wg_mode.setEnabled(True)
        self.wg_coop_players.setEnabled(True)
        self.wg_level_from.setEnabled(True)
        self.wg_level_to.setEnabled(False)
        self.wg_numberofcards.setEnabled(True)
        self.wg_arcade_checkbox.setEnabled(True)
        self.wg_remix_checkbox.setEnabled(True)
        self.wg_fullsong_checkbox.setEnabled(True)
        self.wg_shortcut_checkbox.setEnabled(True)
        self.wg_checkbox_intervals.setEnabled(False)

        for row in self.predefined_rows:
            row["active"].setEnabled(False)
            row["active"].setChecked(False)
            row["steptype"].setEnabled(False)
            row["min"].setEnabled(False)
            row["max"].setEnabled(False)
            row["checkbox"].setEnabled(False)
            row["min"].setText("")
            row["max"].setText("")
            print("Desactivating row")

    def pred_menu_defaults(self):

        if not self.activate_predetermined_checkbox.isChecked():
            return

        checkflag = self.predetermined_settings_combobox.currentText()

        if checkflag == menuText["Settings1"]:
            for row in self.predefined_rows[2:]:
                row["active"].setEnabled(False)
                row["active"].setChecked(False)
                row["steptype"].setEnabled(False)
                row["min"].setEnabled(False)
                row["min"].setText("")
                row["max"].setEnabled(False)
                row["max"].setText("")
                row["checkbox"].setEnabled(False)
                row["checkbox"].setChecked(False)

            for row in self.predefined_rows[:2]:
                row["active"].setChecked(True)
                row["active"].setEnabled(False)

                row["steptype"].setEnabled(True)
                row["min"].setEnabled(True)
                row["checkbox"].setEnabled(True)

            self.predefined_rows[0]["steptype"].setCurrentIndex(0)
            self.predefined_rows[0]["min"].setText("17")

            self.predefined_rows[1]["steptype"].setCurrentIndex(1)
            self.predefined_rows[1]["min"].setText("17")

        if checkflag == menuText["Settings2"]:

            for row in self.predefined_rows[3:]:
                row["active"].setEnabled(False)
                row["active"].setChecked(False)
                row["steptype"].setEnabled(False)
                row["min"].setEnabled(False)
                row["min"].setText("")
                row["max"].setEnabled(False)
                row["max"].setText("")
                row["checkbox"].setEnabled(False)
                row["checkbox"].setChecked(False)

            for row in self.predefined_rows[:3]:
                row["active"].setChecked(True)
                row["active"].setEnabled(False)

                row["steptype"].setEnabled(True)
                row["min"].setEnabled(True)
                row["checkbox"].setEnabled(True)

            self.predefined_rows[0]["steptype"].setCurrentIndex(0)
            self.predefined_rows[0]["min"].setText("20")

            self.predefined_rows[1]["steptype"].setCurrentIndex(1)
            self.predefined_rows[1]["min"].setText("21")

            self.predefined_rows[2]["steptype"].setCurrentIndex(1)
            self.predefined_rows[2]["min"].setText("22")

        if checkflag == menuText["Settings3"]:
            for row in self.predefined_rows[5:]:
                row["active"].setEnabled(False)
                row["active"].setChecked(False)
                row["steptype"].setEnabled(False)
                row["min"].setEnabled(False)
                row["min"].setText("")
                row["max"].setEnabled(False)
                row["max"].setText("")
                row["checkbox"].setEnabled(False)
                row["checkbox"].setChecked(False)

            for row in self.predefined_rows[:5]:
                row["active"].setChecked(True)
                row["active"].setEnabled(False)

                row["steptype"].setEnabled(True)
                row["min"].setEnabled(True)
                row["checkbox"].setEnabled(True)

            self.predefined_rows[0]["steptype"].setCurrentIndex(0)
            self.predefined_rows[0]["min"].setText("22")

            self.predefined_rows[1]["steptype"].setCurrentIndex(1)
            self.predefined_rows[1]["min"].setText("22")

            self.predefined_rows[2]["steptype"].setCurrentIndex(0)
            self.predefined_rows[2]["min"].setText("23")

            self.predefined_rows[3]["steptype"].setCurrentIndex(1)
            self.predefined_rows[3]["min"].setText("24")

            self.predefined_rows[4]["steptype"].setCurrentIndex(1)
            self.predefined_rows[4]["min"].setText("25")

        if checkflag == menuText["Settings4"]:
            for row in self.predefined_rows[3:]:
                row["active"].setEnabled(False)
                row["active"].setChecked(False)
                row["steptype"].setEnabled(False)
                row["min"].setEnabled(False)
                row["min"].setText("")
                row["max"].setEnabled(False)
                row["max"].setText("")
                row["checkbox"].setEnabled(False)
                row["checkbox"].setChecked(False)

            for row in self.predefined_rows[:3]:
                row["active"].setChecked(True)
                row["active"].setEnabled(False)

                row["steptype"].setEnabled(True)
                row["min"].setEnabled(True)
                row["checkbox"].setEnabled(True)

            self.predefined_rows[0]["steptype"].setCurrentIndex(0)
            self.predefined_rows[0]["min"].setText("19")

            self.predefined_rows[1]["steptype"].setCurrentIndex(0)
            self.predefined_rows[1]["min"].setText("18")

            self.predefined_rows[2]["steptype"].setCurrentIndex(0)
            self.predefined_rows[2]["min"].setText("20")

        if checkflag == menuText["Settings5"]:
            for row in self.predefined_rows[5:]:
                row["active"].setEnabled(False)
                row["active"].setChecked(False)
                row["steptype"].setEnabled(False)
                row["min"].setEnabled(False)
                row["min"].setText("")
                row["max"].setEnabled(False)
                row["max"].setText("")
                row["checkbox"].setEnabled(False)
                row["checkbox"].setChecked(False)

            for row in self.predefined_rows[:5]:
                row["active"].setChecked(True)
                row["active"].setEnabled(False)

                row["steptype"].setEnabled(True)
                row["min"].setEnabled(True)
                row["checkbox"].setEnabled(True)

            self.predefined_rows[0]["steptype"].setCurrentIndex(0)
            self.predefined_rows[0]["min"].setText("17")

            self.predefined_rows[1]["steptype"].setCurrentIndex(1)
            self.predefined_rows[1]["min"].setText("18")

            self.predefined_rows[2]["steptype"].setCurrentIndex(0)
            self.predefined_rows[2]["min"].setText("19")

            self.predefined_rows[3]["steptype"].setCurrentIndex(1)
            self.predefined_rows[3]["min"].setText("19")

            self.predefined_rows[4]["steptype"].setCurrentIndex(1)
            self.predefined_rows[4]["min"].setText("20")

        if checkflag == menuText["Settings6"]:
            for row in self.predefined_rows:
                row["active"].setEnabled(True)
                row["active"].setChecked(True)
                row["steptype"].setEnabled(True)
                row["min"].setEnabled(True)
                row["max"].setEnabled(True)
                row["checkbox"].setEnabled(True)
                row["min"].setText("")
                row["max"].setText("")

    def activate_pred_settings(self):
        checkflag = self.activate_predetermined_checkbox.isChecked()
        if checkflag:
            self.predetermined_settings_combobox.setEnabled(True)
            self.deactivate_by_pred()
        else:
            self.predetermined_settings_combobox.setEnabled(False)
            self.activate_by_pred()

    def extract_current_pred_charts(self):
        mode_types = []

        for row in self.predefined_rows:

            if row["active"].isChecked():

                mode_types.append({
                    "steptype": row["steptype"].currentText(),
                    "min":      row["min"].text(),
                    "checkbox": row["checkbox"].isChecked(),
                    "max":      row["max"].text()}
                )
            else:
                print("Ignoring row...")

        print(mode_types)

        return mode_types

    def on_randomizer_event(self):

        if not self.activate_predetermined_checkbox.isChecked():
            self.randomizer.randomize_button(
                self.json_dump,
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
            return

        else:

            info = self.extract_current_pred_charts()
            self.randomizer.randomize_button_predefined(
                self.json_dump,
                info,
                len(info),
                offlinemode=self.wg_offlinemode.isChecked()
            )

# ==============================================================================================================================================
# ==============================================================================================================================================
# ==============================================================================================================================================
# ==============================================================================================================================================
# ==============================================================================================================================================


class APITokenWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout_APIsettings = QVBoxLayout()

        layout_APIkey = QHBoxLayout()
        self.API_info = QLabel("API Key:")
        self.API_lineedit = QLineEdit()
        layout_APIkey.addWidget(self.API_info)
        layout_APIkey.addWidget(self.API_lineedit)

        API_info = QLabel("Please copy here the API token that you can find inside your user profile from PIU scores.\n"
                          "https://piuscores.arroweclip.se/Account -> API")

        self.token_path = Path("api/appcache/token.txt")

        layout_APIkey_buttons = QHBoxLayout()
        layout_APIkey_buttons.setAlignment(Qt.AlignRight)

        self.API_SaveButton = QPushButton("Save API key")
        self.API_Clear = QPushButton("Clear API key")
        self.API_Cancel = QPushButton("Close")

        layout_APIkey_buttons.addWidget(self.API_SaveButton)
        layout_APIkey_buttons.addWidget(self.API_Clear)
        layout_APIkey_buttons.addWidget(self.API_Cancel)

        main_layout_APIsettings.addLayout(layout_APIkey)
        main_layout_APIsettings.addWidget(API_info)
        main_layout_APIsettings.addLayout(layout_APIkey_buttons)

        self.setLayout(main_layout_APIsettings)

        self.setWindowTitle("API Settings")
        self.resize(500, 100)

        self.API_Cancel.clicked.connect(
            self.API_closewindow)

        self.API_Clear.clicked.connect(
            self.API_cleartext)

        self.API_SaveButton.clicked.connect(
            self.API_savetoken)

        # self.token_exists()
        # self.block_text_ifAPI()
        self.update_token_state()

    def API_closewindow(self):
        self.close()

    def API_cleartext(self):
        self.token_path.unlink(missing_ok=True)
        self.API_lineedit.clear()
        self.update_token_state()

    def API_savetoken(self):
        token = self.API_lineedit.text()

        with open(self.token_path, "w", encoding="utf-8") as f:
            f.write(token)

        self.update_token_state()

        self.token_ok_message = QMessageBox.information(self,
                                                        "API Token",
                                                        "Token updated successfully")
        return self.token_path

    def update_token_state(self):
        if self.token_path.exists():
            token = self.token_path.read_text(encoding="utf-8").strip()

            if token:
                masked = f"{token[:4]}{'*' * (len(token) - 8)}{token[-4:]}"
                self.API_lineedit.setText(masked)
                self.API_lineedit.setEnabled(False)
                self.API_SaveButton.setEnabled(False)
                return

        self.API_lineedit.clear()
        self.API_lineedit.setEnabled(True)
        self.API_SaveButton.setEnabled(True)


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
