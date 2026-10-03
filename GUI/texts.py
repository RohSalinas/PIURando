cacheText = {
    "ReloadCache": "Do you want to reload the image cache for the songscards?. This will download all songcards locally for offline usage.\n\n"
    "This requires your PIUScores API token and internet connection (About 200MB of space if done the first time)\n\n"
    "It is recommended to run this after every PIU update to also add new songs and charts. Do you want to proceed?",

    "DeleteCache": "Do you want to delete the cache for the songscards? This includes user token information.\n\n"
    "This action cannot be undone, and can only be fixed by downloading the cache again which requires internet connection.\n\n"
    "(About 200MB of space). Do you want to proceed?",

    "FirstTime": "There is no cache detected for the song cards in this computer.\n\n"
    "For running tournaments and for an offline experience, it is recommended to download the song cards cache for visualization.\n\n"
    "This requires your PIUScores API token and internet connection (About 200MB the first time).\n\n"
    "If you proceed, the API key windows will pop up to input your token. Do you want to proceed?",

    "Off_to_OnlineMode_cache": "You are changing to 'Online Mode'. Local cache files were detected in your system.\n\n"
    "The application will work and only use internet data if a song not present in the cache is chosen (Usually new songs not yet updated in the cache).",

    "Off_to_OnlineMode_nocache": "You are changing to 'Online Mode' with no cache files downloaded locally.\n\n"
    "If you proceed, the application will work, but it will consume internet data every time a song is randomized.\n\n"
    "It is recommended to download the cache previously with internet connection to mitigated this.",

    "On_to_OfflineMode_nocache": "You are changing to 'Offline Mode' with no cache files downloaded locally.\n\n"
    "For 'Offline mode', please perform a local cache installation (Menu -> Reload Song Cache).\n\n"
    "This requires internet connection (About 200MB the first time)."
}

menuText = {
    "Settings1": "Tournament - Single and Double round",
    "Settings2": "Tournament - Best of 3 Round",
    "Settings3": "Tournament - Best of 5 Round",
    "Settings4": "1 Normal Credit (3 Arcade Songs)",
    "Settings5": "1 Premium Credit (5 Arcade Songs)",
    "Settings6": "Custom Individual charts (Use left checkboxs)"
}


stylesheets = {
    "defaultLevel": """
            QLabel {
                color: white;
                background-color: black;
                font-size: 22px;
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
                font-size: 30px;
                font-weight: bold;
                padding: 10px;
                border-radius:10px;
            }
            """,
    "redStyle": """
            QLabel {
                color: white;
                background-color: red;
                font-size: 30px;
                font-weight: bold;
                padding: 10px;
                border-radius:10px;
            }
            """,
    "coopStyle": """
            QLabel {
                color: black;
                background-color: yellow;
                font-size: 30px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
            """,
    "randomize": """
            QPushButton {
                color: white;
                background-color: blue;
                font-size: 25px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
            """,

    "MainSettings": """
            QLabel {
                color: white;
                outline-color: black;
                background-color: rgb(0, 76, 153);
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
                border-radius: 2px;
                text-align: center;
            }
            """,
    "SecSettings": """
            QLabel {
                color: white;
                outline-color: black;
                background-color: rgb(0, 102, 204);
                font-size: 15px;
                font-weight: bold;
                padding: 10px;
                border-radius: 2px;
                text-align: center;
            }
            """
}
