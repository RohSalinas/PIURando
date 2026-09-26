from filters.randsong import randomize_chart
from PySide6.QtCore import QObject, Signal
from pathlib import Path


class RandomizerButton(QObject):

    error_nominlvl = Signal()
    error_minovermax = Signal()

    randomize_over = Signal()

    imagechange = Signal(str)

    def __init__(self):
        super().__init__()
        self.cachefolder = Path("api/appcache/songcards/")
        self.randomchart = None
        self.songcardname = ""

    def randomize_button(self, json_single, json_double, mode, fromlvl, tolvl, n_songs, subsettings, maxlevel=False):

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

        if mf["type"] == "Single":
            self.random_chart = randomize_chart(json_single, mf, subsettings)

        if mf["type"] == "Double":
            self.random_chart = randomize_chart(json_double, mf, subsettings)

        imageurl = self.random_chart["song"]["imagePath"]
        self.songcardname = Path(imageurl).name

        print(self.random_chart)
        print(imageurl)
        print(self.songcardname)

        self.randomize_over.emit()

    def assign_chart_to_image(self):
        path_to_random = Path(f"api/appcache/songcards") / self.songcardname
        self.imagechange.emit(str(path_to_random))
