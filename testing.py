import random
from pathlib import Path

from filters.filtering import filter_bycategory, filter_bytype, filter_bylevel
from api.api_maincall import load_json

JSONPATH_SINGLE = load_json(Path("api/appcache/dump_Single.json"))
JSONPATH_DOUBLE = load_json(Path("api/appcache/dump_Double.json"))


def randomize_chart(json_data, main_filters, sub_filters):
    """
    Main randomizer tool. Uses filter helpers to generate a final list from which a random song is then selected.

    Parameters
        json_data: Path
            Path to the current dump of the API with all chart information
        main_filters: dict
            Dictionary with the main filters selected from the user (Type of chart and levels)
        sub_filters: dict
            Dictionary with sub-filters selected from the user (Category of the chart)
    """

    filter1 = filter_bytype(json_data, main_filters["type"])
    filter2 = filter_bylevel(filter1, main_filters["level"])
    filter3 = filter_bycategory(filter2, sub_filters)

    random_chart = random.choice(filter3)
    print(
        f"Song Selected: {random_chart["song"]["name"]} || Level: {random_chart["shorthand"]} ")

    return random_chart


mf = {"type": "Double",
      "level": 18}

sf = {"arcade": False,
      "shortcut": False,
      "fullsong": False,
      "remix": False
      }

randochart = randomize_chart(JSONPATH_DOUBLE, mf, sf)
