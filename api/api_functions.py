from filters.randsong import randomize_chart
from PySide6.QtCore import QObject, Signal
from pathlib import Path

from api.api_maincall import get_charts_info, download_image


class RandomizerButton(QObject):

    error_nominlvl = Signal()
    error_minovermax = Signal()
    error_nolevel = Signal()

    randomize_over = Signal()

    imagechange = Signal(str)
    levelchange = Signal(str)

    def __init__(self):
        super().__init__()
        self.cachefolder = Path("api/appcache/songcards/")
        self.randomchart = None
        self.songcardname = ""
        self.songlevel = ""
        self.GREEN_LEVEL_STYLE = """
            QLabel {
                color: white;
                background-color: green;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
            """

        self.RED_LEVEL_STYLE = """
                QLabel {
                    color: white;
                    background-color: red;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 10px;
                }
                """
        self.COOP_LEVEL_STYLE = """
                QLabel {
                    color: black;
                    background-color: yellow;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 10px;
                }
                """

    def randomize_button(self, json_all, mode, fromlvl, tolvl, n_songs, subsettings, n_persons, maxlevel=False, offlinemode=True):

        if not offlinemode:
            APPCACHE_DIR = Path("api/appcache/songcards")
            output_dir = APPCACHE_DIR
            output_dir.parent.mkdir(parents=True, exist_ok=True)
            get_charts_info()

        if mode == "Co-Op":
            CoOp_flag = "CoOp"
            CoOp_n_persons = str(n_persons)

            mf = {
                "type": CoOp_flag,
                "persons": CoOp_n_persons
            }

            self.random_chart = randomize_chart(json_all, mf, subsettings)

            if self.random_chart is None:
                self.error_nolevel.emit()
                return
        else:
            if tolvl:
                int_tolvl = int(tolvl)
            else:
                int_tolvl = None

            if not fromlvl:
                self.error_nominlvl.emit()
                return

            int_fromlvl = int(fromlvl)
            int_n_songs = int(n_songs)

            if int_tolvl is not None and int_fromlvl > int_tolvl:
                self.error_minovermax.emit()
                return

            mf = {
                "type": mode,
                "level": int_fromlvl,
                "maxlevel": int_tolvl,
                "maxlevelflag": maxlevel,
                "n_songs": int_n_songs,
            }

            self.random_chart = randomize_chart(json_all, mf, subsettings)

            if self.random_chart is None:
                self.error_nolevel.emit()
                return

        imageurl = self.random_chart["song"]["imagePath"]
        if not offlinemode:
            download_image(self.random_chart, output_dir)

        self.songcardname = Path(imageurl).name
        self.songlevel = self.random_chart["shorthand"]

        # print(self.random_chart)
        # print(imageurl)
        # print(self.songcardname)

        self.randomize_over.emit()

    def assign_chart_to_image(self):
        path_to_random = Path(f"api/appcache/songcards") / self.songcardname
        self.imagechange.emit(str(path_to_random))

        if "C" in self.songlevel:
            final_label = f"Co-Op x {self.songlevel[-1]}"
            self.levelchange.emit(str(final_label))
        else:
            self.levelchange.emit(str(self.songlevel))
