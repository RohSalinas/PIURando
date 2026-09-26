from pathlib import Path
import random

from api.api_maincall import load_json

"""
Filters are applied from a mayor to a lower hierarchy.
Type -> Level -> Category
"""


def filter_bytype(json_data, type):
    filtered_results = []

    for chart in json_data["results"]:
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
        if chart["song"]["type"].lower() in true_filters:
            filtered_results.append(chart)

    return filtered_results  # List with dict
