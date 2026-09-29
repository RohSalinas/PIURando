cacheText = {
    "ReloadCache": "Do you want to reload the image cache for the songscards?. This will download all songcards locally for offline usage. This requires internet connection.\n\n"
    "(About 200MB of space if done the first time)\n\n"
    "It is recommended to run this after every PIU update to also add new songs and charts.",

    "DeleteCache": "Do you want to delete the image cache for the songscards?.\n\n"
    "This action cannot be undone, and can only be fixed by downloading the cache again which requires internet connection.\n\n"
    "(About 200MB of space)",

    "FirstTime": "There is no cache detected for the song cards in this computer.\n\n"
    "For running tournaments and for an offline experience, it is recommended to download the song cards cache for visualization.\n\n"
    "This requires internet connection (About 200MB the first time). Do you want to proceed?",

    "Off_to_OnlineMode_cache": "You are changing to 'Online Mode'. Local cache files were detected in your system.\n\n"
    "The application will work and only use internet data if a song not present in the cache is chosen (Usually new songs not yet updated in the cache).",

    "Off_to_OnlineMode_nocache": "You are changing to 'Online Mode' with no cache files downloaded locally.\n\n"
    "If you proceed, the application will work, but it will consume internet data every time a song is randomized.\n\n"
    "It is recommended to download the cache previously with internet connection to mitigated this.",

    "On_to_OfflineMode_nocache": "You are changing to 'Offline Mode' with no cache files downloaded locally.\n\n"
    "For 'Offline mode', please perform a local cache installation (Menu -> Reload Song Cache).\n\n"
    "This requires internet connection (About 200MB the first time)."
}


stylesheets = {
    "defaultLevel": """
            QLabel {
                color: white;
                background-color: black;
                font-size: 18px;
                font-weight: bold;
                font-style: italic;
                padding: 10px;
                border-radius:10px;
            }
            """,
    "greenStyle": """
            QLabel {
                color: white;
                background-color: green;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border-radius:10px;
            }
            """,
    "redStyle": """
            QLabel {
                color: white;
                background-color: red;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border-radius:10px;
            }
            """,
    "coopStyle": """
            QLabel {
                color: black;
                background-color: yellow;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
            """,
    "randomize": """
            QPushButton {
                color: white;
                background-color: blue;
                font-size: 30px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
            """,
}
