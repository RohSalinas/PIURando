import csv
from pathlib import Path

"""
Filters are applied from a mayor to a lower hierarchy.
Type -> Level -> Category
"""


def filter_bytype(json_data, type):
    filtered_results = []

    for chart in json_data["data"]:
        if type == chart["type"]:
            filtered_results.append(chart)
    return filtered_results  # List with dicts


def filter_bylevel(filtered_listwdict, min_level, max_level=None, max=False):
    filtered_results = []

    if not max:
        for chart in filtered_listwdict:
            if min_level == chart["level"]:
                filtered_results.append(chart)

    if max:
        for chart in filtered_listwdict:
            if min_level <= chart["level"] <= max_level:
                filtered_results.append(chart)

    return filtered_results  # List with dit


def filter_bycategory(filtered_listwdict, categoryfilterdict):
    true_filters = []
    filtered_results = []

    for category, filter in categoryfilterdict.items():
        if filter:
            true_filters.append(category)

    if not true_filters:
        return filtered_listwdict  # List with dict

    for chart in filtered_listwdict:
        # if chart["song"]["type"].lower() in true_filters:
        if chart["songType"].lower() in true_filters:
            filtered_results.append(chart)

    return filtered_results  # List with dict


def filter_coop(json_data, type, n_persons, tier, tierflag=False):
    filtered_results = []
    true_filters = []

    for chart in json_data["data"]:
        if type == chart["type"]:
            filtered_results.append(chart)

    if n_persons == "any":
        if tierflag:
            cooptiers = load_cooptiers()
            print(cooptiers)
            print("="*60)
            current_tier_list = [
                song for song in cooptiers if song["tier"] == tier]

            print(current_tier_list)

            for chart in filtered_results:
                if any(song["songName"] == chart["songName"] for song in current_tier_list):
                    true_filters.append(chart)
            print(true_filters)
            return true_filters
        else:
            return filtered_results  # List with dicts

    else:
        coop_n = f"{type}{n_persons}"

        if tierflag:
            cooptiers = load_cooptiers()
            current_tier_list = [
                song for song in cooptiers if song["tier"] == tier and song["difficulty"] == coop_n]
            for chart in filtered_results:
                if any(song["songName"] == chart["songName"] for song in current_tier_list):
                    true_filters.append(chart)
            return true_filters
        else:

            for chart in filtered_results:
                if chart["difficulty"] == coop_n:
                    true_filters.append(chart)

        # with open(f"coop_{n_persons}players.json", "w", encoding="utf-8") as f:
        #     json.dump(true_filters, f, indent=4)

        return true_filters


def load_cooptiers():
    CSV_PATH = Path("api/coop_songs.csv")

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        coop_tiers = list(csv.DictReader(f))

    return coop_tiers
