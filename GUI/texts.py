from GUI.resource_paths import asset_url

print(asset_url("options1.png"))

cacheText = {
    "ReloadCache": "Do you want to reload the image cache for the songscards?. This will download all songcards locally for offline usage.\n\n"
    "This requires your PIUScores API token and internet connection (About 200MB of space if done the first time)\n\n"
    "It is recommended to run this after every PIU update to also add new songs and charts. Do you want to proceed?",

    "DeleteCache": "Do you want to delete the cache for the songscards? This doesn't include your API token information.\n\n"
    "This action cannot be undone. You can re-download the cache again anytime, which requires internet connection.\n\n"
    "(About 200MB of space). Do you want to proceed?",

    "FirstTime": "There is no cache detected for the song cards in this computer.\n\n"
    "For running tournaments and for an offline experience, it is recommended to download the song cards cache beforehand for visualization.\n\n"
    "This requires your PIUScores API token and internet connection (About 200MB the first time).\n\n"
    "If you proceed, the API key windows will pop up to input your token. Do you want to proceed?",

    "Off_to_OnlineMode_cache": "You are changing to 'Online Mode'. Local cache files were detected in your system.\n\n"
    "The application will work and only use internet data if a song not present in the cache is selected (Usually new songs not yet updated in the cache).",

    "Off_to_OnlineMode_nocache": "You are changing to 'Online Mode' with no cache files downloaded locally.\n\n"
    "If you proceed, the application will work, but it will consume internet data every time a song is randomized.\n\n"
    "It is recommended to download the cache previously to mitigated this and to be up to date with song charts.",

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

aboutText = """
<h2><b>Pump it Up Randomizer</b></h2>
- Created by <b><p style="color: cyan;">RoHiSakk</p></b>
- API integration from
<a href="https://piuscores.arroweclip.se">PIUScores API</a><br>
(Special thanks to Dr. Murloc for maintaining it!)<br><br>
- Co-Op tierlist based on
<a href="https://arcadestat.app/en/pump/tier/c2">ArcadeStat</a>
    """

stylesheets = {
    "defaultLevel": """
            QLabel {
                color: white;
                font-family: "Oswald";
                background-color: black;
                font-size: 22px;
                font-weight: bold;
                padding: 10px;
                border-radius:10px;
            }
            """,
    "greenStyle": """
            QLabel {
                color: white;
                background-color: green;
                font-family: "Oswald";
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
                font-family: "Oswald";
                font-weight: bold;
                padding: 10px;
                border-radius:10px;
            }
            """,
    "coopStyle": """
            QLabel {
                color: black;
                background-color: yellow;
                font-size: 20px;
                font-family: "Oswald";
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
            """,
    "randomize": """
            QPushButton {
                color: white;
                font-family: "Oswald";
                background-color: #1eba2b;
                font-size: 40px;
                font-weight: bold;
                border: 5px #096b0c;
                border-radius: 15px;
                padding: 10px;
                border-radius: 10px;
            }

            QPushButton:hover{
                border: 3px solid white;
                }

            QPushButton:pressed{
                background-color: #096b0c;
                }

            """,

    "MainSettings": """
            QLabel {
                background-image: url("{OPTIONS_IMAGE}");
                background-position: center;
                background-repeat: no-repeat;
                font-family: "Oswald";
                color: white;
                outline-color: black;
                background-color: rgb(0, 76, 153);
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
                border-radius: 2px;
                text-align: center;
            }
            """.replace(
                "{OPTIONS_IMAGE}",
                asset_url("options1.png")
    ),
    "SecSettings": """
            QLabel {
                background-image: url("{OPTIONS_IMAGE2}");
                background-position: center;
                background-repeat: no-repeat;
                color: white;
                font-family: "Oswald";
                outline-color: black;
                background-color: rgb(0, 102, 204);
                font-size: 15px;
                font-weight: bold;
                padding: 10px;
                border-radius: 2px;
                text-align: center;
            }
            """.replace(
        "{OPTIONS_IMAGE2}",
        asset_url("options1.png")
    )
}
