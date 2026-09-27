from filters.randsong import randomize_chart
from PySide6.QtCore import QObject, Signal
from pathlib import Path

from api.api_maincall import get_charts_info, download_image


class RandomizerButton(QObject):

    error_nominlvl = Signal()
    error_minovermax = Signal()
    error_nolevel = Signal()

    randomize_over = Signal()

    imagechange = Signal(list)
    levelchange = Signal(list)
    newcharts_ok = Signal(list)

    def __init__(self):
        super().__init__()
        self.cachefolder = Path("api/appcache/songcards/")
        self.randomchart = None
        self.songcardname = ""
        self.songlevel = ""
        self.allcharts = []
        self.nsongs = None

    def randomize_button(self, json_all, mode, fromlvl, tolvl, n_songs, subsettings, n_persons, maxlevel=False, offlinemode=True):

        self.allcharts.clear()

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

            imageurl = self.random_chart["song"]["imagePath"]
            if not offlinemode:
                download_image(self.random_chart, output_dir)

            self.songcardname = Path(imageurl).name
            self.songlevel = self.random_chart["shorthand"]

            chart_dict = {"level": self.songlevel,
                          "image": self.songcardname}

            self.allcharts.append(chart_dict)

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
            self.nsongs = int_n_songs

            if int_tolvl is not None and int_fromlvl > int_tolvl:
                self.error_minovermax.emit()
                return

            mf = {
                "type": mode,
                "level": int_fromlvl,
                "maxlevel": int_tolvl,
                "maxlevelflag": maxlevel,
            }

            for i in range(int_n_songs):
                self.random_chart = randomize_chart(json_all, mf, subsettings)

                if self.random_chart is None:
                    self.error_nolevel.emit()
                    return

                imageurl = self.random_chart["song"]["imagePath"]
                if not offlinemode:
                    download_image(self.random_chart, output_dir)

                self.songcardname = Path(imageurl).name
                self.songlevel = self.random_chart["shorthand"]

                chart_dict = {"level": self.songlevel,
                              "image": self.songcardname}

                self.allcharts.append(chart_dict)

        self.randomize_over.emit()

    def assign_chart_to_image(self):
        updated_charts = []

        for chart in self.allcharts:
            path_to_random = Path(
                f"api/appcache/songcards") / chart["image"]

            if "C" in chart["level"]:
                final_label = f"Co-Op x {chart["level"][-1]}"
            else:
                final_label = chart["level"]

            updated_charts.append({
                "image": path_to_random,
                "level": final_label
            })

        print(updated_charts)

        self.newcharts_ok.emit(updated_charts)

        # self.imagechange.emit(image_paths)
        # self.levelchange.emit(levels)
