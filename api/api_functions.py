from filters.randsong import randomize_chart
from PySide6.QtCore import QObject, Signal
from pathlib import Path

from api.api_maincall import download_image, get_charts_info_v2


class RandomizerButton(QObject):

    error_nominlvl = Signal()
    error_minovermax = Signal()
    error_nolevel = Signal()
    error_notenoughcharts = Signal(int, int)
    error_nomaxlevel_whentrue = Signal()

    randomize_over = Signal()

    imagechange = Signal(list)
    levelchange = Signal(list)
    newcharts_ok = Signal(list)

    def __init__(self):
        super().__init__()
        self.cachefolder = Path("api/appcache/songcards/")
        self.randomchart = None
        self.filterlen = None
        self.songcardname = ""
        self.songlevel = ""
        self.allcharts = []
        self.nsongs = None
        self.selected = set()

    def randomize_button(self, json_all, mode, fromlvl, tolvl, n_songs, subsettings, n_persons, maxlevel=False, offlinemode=True):

        self.allcharts.clear()

        if not offlinemode:
            APPCACHE_DIR = Path("api/appcache/songcards")
            output_dir = APPCACHE_DIR
            output_dir.parent.mkdir(parents=True, exist_ok=True)
            output_cache = Path(f"api/appcache/dump_all_v2.json")
            if not output_cache:
                # get_charts_info()
                get_charts_info_v2(mix="phoenix2")

        if mode == "Co-Op":
            CoOp_flag = "CoOp"
            CoOp_n_persons = str(n_persons)

            mf = {
                "type": CoOp_flag,
                "persons": CoOp_n_persons
            }

            self.random_chart, self.filterlen = randomize_chart(
                json_all, mf, subsettings)

            if self.random_chart is None:
                self.error_nolevel.emit()
                return

            # imageurl = self.random_chart["song"]["imagePath"]
            imageurl = self.random_chart["imageUrl"]
            if not offlinemode:
                download_image(self.random_chart, output_dir)

            self.songcardname = Path(imageurl).name
            # self.songlevel = self.random_chart["shorthand"]
            self.songlevel = self.random_chart["difficulty"]

            chart_dict = {"level": self.songlevel,
                          "image": self.songcardname}

            self.allcharts.append(chart_dict)

        else:

            if tolvl:
                int_maxlvl = int(tolvl)
            else:
                int_maxlvl = None

            if not fromlvl or fromlvl == 0:
                self.error_nominlvl.emit()
                return

            int_minlvl = int(fromlvl)
            int_n_songs = int(n_songs)
            self.nsongs = int_n_songs

            if int_maxlvl is not None and int_minlvl > int_maxlvl:
                self.error_minovermax.emit()
                return

            if maxlevel and not int_maxlvl:
                self.error_nomaxlevel_whentrue.emit()
                return

            mf = {
                "type": mode,
                "level": int_minlvl,
                "maxlevel": int_maxlvl,
                "maxlevelflag": maxlevel,
            }

            attempts = 0
            self.selected.clear()

            while attempts < int_n_songs:

                for i in range(int_n_songs):
                    self.random_chart, self.filterlen = randomize_chart(
                        json_all, mf, subsettings)

                    if self.random_chart is None:
                        self.error_nolevel.emit()
                        return

                    if self.filterlen < int_n_songs:
                        self.error_notenoughcharts.emit(
                            int_n_songs, self.filterlen)
                        return

                    # imageurl = self.random_chart["song"]["imagePath"]
                    imageurl = self.random_chart["imageUrl"]
                    if not offlinemode:
                        download_image(self.random_chart, output_dir)

                    self.songcardname = Path(imageurl).name
                    self.songlevel = self.random_chart["difficulty"]

                    chart_dict = {"level": self.songlevel,
                                  "image": self.songcardname}

                    if self.songcardname in self.selected:
                        print(f"Repetida: {self.songcardname}")
                        print(f"Contador: {attempts}")
                        break

                    self.selected.add(self.songcardname)
                    self.allcharts.append(chart_dict)
                    attempts += 1

        self.randomize_over.emit()

    def randomize_button_predefined(self, json_all, allchartsinfo, n_songs, offlinemode=True):

        self.allcharts.clear()
        print(n_songs)

        if not offlinemode:
            APPCACHE_DIR = Path("api/appcache/songcards")
            output_dir = APPCACHE_DIR
            output_dir.parent.mkdir(parents=True, exist_ok=True)
            output_cache = Path(f"api/appcache/dump_all_v2.json")
            if not output_cache:
                # get_charts_info()
                get_charts_info_v2(mix="phoenix2")

        for chart in allchartsinfo:

            if chart["max"]:
                int_maxlvl = int(chart["max"])
            else:
                int_maxlvl = None

            if not chart["min"]:
                self.error_nominlvl.emit()
                return

            int_minlvl = int(chart["min"])
            int_n_songs = int(n_songs)
            self.nsongs = int_n_songs

            print(int_n_songs)

            if int_maxlvl is not None and int_minlvl > int_maxlvl:
                self.error_minovermax.emit()
                return

            if chart["checkbox"] and not int_maxlvl:
                self.error_nomaxlevel_whentrue.emit()
                return

            mf = {
                "type": chart["steptype"],
                "level": int_minlvl,
                "maxlevel": int_maxlvl,
                "maxlevelflag": chart["checkbox"],
            }

            attempts = True
            self.selected.clear()

            while attempts:

                # for i in range(int_n_songs):
                self.random_chart, self.filterlen = randomize_chart(
                    json_all, mf, sub_filters={'arcade': True, 'shortcut': False, 'fullsong': False, 'remix': False})

                if self.random_chart is None:
                    self.error_nolevel.emit()
                    return

                if self.filterlen < int_n_songs:
                    self.error_notenoughcharts.emit(
                        int_n_songs, self.filterlen)
                    return

                imageurl = self.random_chart["imageUrl"]
                # imageurl = self.random_chart["song"]["imagePath"]
                if not offlinemode:
                    download_image(self.random_chart, output_dir)

                self.songcardname = Path(imageurl).name
                self.songlevel = self.random_chart["difficulty"]

                chart_dict = {"level": self.songlevel,
                              "image": self.songcardname}

                if self.songcardname in self.selected:
                    print(f"Repetida: {self.songcardname}")
                    print(f"Contador: {attempts}")
                    break

                self.selected.add(self.songcardname)
                self.allcharts.append(chart_dict)
                attempts = False

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
