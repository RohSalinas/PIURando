from filters.randsong import randomize_chart
from PySide6.QtCore import QObject, Signal


class RandomizerButton(QObject):

    error_nominlvl = Signal()
    error_minovermax = Signal()

    def __init__(self):
        super().__init__()

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

        # print("Printing mf")
        # print(mf)
        # print("Printing variables")
        # print(mode, int_fromlvl, int_tolvl, int_n_songs)
        # print("Printing variables types")
        # print(type(mode), type(int_fromlvl), type(int_tolvl), type(int_n_songs))

        if mf["type"] == "Single":
            randomize_chart(json_single, mf, subsettings)
        if mf["type"] == "Double":
            randomize_chart(json_double, mf, subsettings)


# def randomize_button(json_single, json_double, mode, fromlvl, tolvl, n_songs, subsettings, maxlevel=False):
#     error = Signal(str)

#     if tolvl:
#         int_tolvl = int(tolvl)
#     else:
#         int_tolvl = None

#     if not int_tolvl:
#         return

#     int_fromlvl = int(fromlvl)
#     int_n_songs = int(n_songs)

#     mf = {
#         "type": mode,
#         "level": int_fromlvl,
#         "maxlevel": int_tolvl,
#         "maxlevelflag": maxlevel,
#         "n_songs": int_n_songs,
#     }

#     # print("Printing mf")
#     # print(mf)
#     # print("Printing variables")
#     # print(mode, int_fromlvl, int_tolvl, int_n_songs)
#     # print("Printing variables types")
#     # print(type(mode), type(int_fromlvl), type(int_tolvl), type(int_n_songs))

#     if mf["type"] == "Single":
#         randomize_chart(json_single, mf, subsettings)
#     if mf["type"] == "Double":
#         randomize_chart(json_double, mf, subsettings)
