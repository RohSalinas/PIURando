import requests
import json
from pathlib import Path

BASE_URL = "https://piuscores.arroweclip.se"

# My token, needs to be replaced later
TOKEN = "OjQ1YzU5YjQ4LTZjODctNGRjMi05NDY2LTlmYjUzM2ZlODQ3MQ=="
HEADERS = {
    "Authorization": f"Basic {TOKEN}",
    "Accept": "*/*",
}
# Helper function to print JSON in a readable way


def pretty(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ── Fetch charts with filters ───────────────────────────────────────────────────
def get_charts(mix=None, chart_type=None, level=None, page=1, count=10):
    """
    Fetch charts from /api/charts with optional filters.

    Parameters:
        mix        : Game version string, e.g. "Phoenix", "XX", "Fiesta2"
        chart_type : "Single" or "Double"
        level      : int (1 to 29)
        page       : page number (starts at 1)
        count      : results per page (max seems to be 50)
    """
    # Build dictionaty with information of charts retrieved
    params = {"Page": page, "Count": count}

    if mix:
        params["Mix"] = mix
    if chart_type:
        params["ChartType"] = chart_type
    if level is not None:
        params["Level"] = level

    response = requests.get(
        f"{BASE_URL}/api/charts",   # ← lowercase 'charts'!
        headers=HEADERS,
        params=params
    )

    print(f"Status : {response.status_code}")
    print(f"URL    : {response.url}\n")

    output_file = Path(f"api/dump_{page}.json")

    if response.ok:

        charts = response.json()

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(charts, f, indent=4, ensure_ascii=False)

        return response.json()

    else:
        print("Error response:", response.text)
        return None


# ── Fetch ALL charts for a given filter (handles pagination) ────────────────────
def get_all_charts(mix=None, chart_type=None, level=None, count_per_page=50):
    """
    Loops through all pages and returns a flat list of every chart matching
    the filters. Useful for building a full local pool for the randomizer.
    """
    all_results = []
    page = 1

    while True:
        data = get_charts(mix=mix, chart_type=chart_type, level=level,
                          page=page, count=count_per_page)
        if not data or not data.get("results"):
            break

        batch = data["results"]
        all_results.extend(batch)

        total = data.get("totalResults", 0)
        print(
            f"  Page {page}: got {len(batch)} charts | total so far: {len(all_results)} / {total}")

        if len(all_results) >= total:
            break
        page += 1

    return all_results


# ── Summarise a list of chart objects ──────────────────────────────────────────
def summarise(charts):
    print(f"\n── Summary: {len(charts)} charts ──")
    for c in charts:
        song = c.get("song", {})
        print(
            f"  [{c.get('shorthand', '?')}]  {song.get('name', '?')}  ({song.get('type', '?')})")
        print(f"         Image: {song.get('imagePath', '')}")


# ── Main ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Test 1: Single page of D20 charts from Phoenix
    print("=== Test 1: D20 charts from Phoenix (1 page) ===")
    data = get_charts(mix="Phoenix", chart_type="Double",
                      level=20, count=5)
    if data:
        print(f"Total matching charts in DB: {data['totalResults']}")
        pretty(data)

    # Test 2: All S17 charts from Phoenix (auto-paginates)
    print("\n=== Test 2: ALL S17 Single charts from Phoenix ===")
    charts = get_all_charts(
        mix="Phoenix", chart_type="Single", level=17)
    if charts:
        summarise(charts)

    # Test 3: No filter — grab a broad sample (useful to explore what Mixes exist)
    print("\n=== Test 3: First 10 charts with no filter ===")
    data = get_charts(count=10)
    if data:
        pretty(data)


def get_all_charts_art(mix=None, chart_type=None, level=None, count_per_page=50):
    """
    Loops through all pages and returns a flat list of every chart matching
    the filters. Useful for building a full local pool for the randomizer.
    """
    all_results = []
    page = 1

    while True:
        data = get_charts(mix=mix, chart_type=chart_type, level=level,
                          page=page, count=count_per_page)
        if not data or not data.get("results"):
            break

        batch = data["results"]
        all_results.extend(batch)

        total = data.get("totalResults", 0)
        print(
            f"  Page {page}: got {len(batch)} charts | total so far: {len(all_results)} / {total}")

        if len(all_results) >= total:
            break
        page += 1

    return all_results
