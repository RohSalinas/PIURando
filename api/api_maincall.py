import requests
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import os

BASE_URL = "https://piuscores.arroweclip.se"  # Website

# ===================================================
# My token, needs to be replaced later
TOKEN = "OjQ1YzU5YjQ4LTZjODctNGRjMi05NDY2LTlmYjUzM2ZlODQ3MQ=="
HEADERS = {
    "Authorization": f"Basic {TOKEN}",
    "Accept": "*/*",
}

# ===================================================

APPCACHE_DIR = Path("api/appcache/songcards")


def get_charts_info(mix=None, chart_type=None, level=None, count=False, max_count=4):
    """
    Fetch charts from /api/charts with optional filters.

    Parameters:
        mix        : Game version string, e.g. "Phoenix", "XX", "Fiesta2"
        chart_type : "Single" or "Double"
        level      : int (1 to 29)
        count      : Max number of charts to fetch from the API
    """
    # Build dictionaty with information of charts retrieved
    # Max charts logic
    if count:
        params = {"Count": max_count}
    else:
        params = {"Count": 9999}

    # Mix, type and level
    if mix:
        params["Mix"] = mix
    if chart_type:
        params["ChartType"] = chart_type
    if level is not None:
        params["Level"] = level

    # API request
    response = requests.get(
        f"{BASE_URL}/api/charts",
        headers=HEADERS,
        params=params
    )

    # Check API status
    print(f"Status : {response.status_code}")
    print(f"URL    : {response.url}\n")

    # Output dir
    output_file = Path(f"api/dump_{chart_type}_{level}.json")

    # Retrieval if API ok
    if response.ok:

        charts = response.json()

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(charts, f, indent=4, ensure_ascii=False)

        return response.json()

    else:
        print("Error response:", response.text)
        return None


def load_json(file_path):
    with open(file_path) as f:
        json_file = json.load(f)
        return json_file


def download_image(chart, output_dir):

    image_url = chart["song"]["imagePath"]
    filename = Path(image_url).name

    output_path = output_dir / filename

    if output_path.exists():
        return

    try:

        response = requests.get(image_url, timeout=15)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)

        return True

    except requests.RequestException as e:
        print(f"Failed: {image_url} -> {e}")
        return False


def download_image_cache(json_file):

    charts = load_json(json_file)

    output_dir = APPCACHE_DIR
    output_dir.parent.mkdir(parents=True, exist_ok=True)

    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = [
            executor.submit(download_image, chart, output_dir)
            for chart in charts["results"]
        ]

        for future in futures:
            future.result()


def delete_cache():
    output_dir = APPCACHE_DIR

    for songcard in output_dir.iterdir():
        if songcard.name.endswith(".png"):
            songcard.unlink()
