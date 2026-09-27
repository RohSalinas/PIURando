import requests
import json
from pathlib import Path

from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from PySide6.QtCore import QObject, Signal
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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


# Create this once, reuse across all workers
_session = requests.Session()
_retry_strategy = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
_adapter = HTTPAdapter(max_retries=_retry_strategy)
_session.mount("https://", _adapter)
_session.mount("http://", _adapter)


def get_charts_info(mix=None, chart_type=None, level=None, count=False, max_count=4):
    """
    Fetch charts from /api/charts with optional filters and save a dump JSON file.

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
        params = {"Count": 99999}

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
    if not chart_type:
        output_file = Path(f"api/appcache/dump_all.json")
    else:
        output_file = Path(f"api/appcache/dump_{chart_type}.json")

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
    """
    Load JSON files

    Parameteres:
        file_path: Path
            JSON dump file path

    Returns:
        JSON file as a python dict    
    """

    with open(file_path) as f:
        json_file = json.load(f)
        return json_file


def download_image(chart, output_dir):
    """
    Single iteration for downloading an image using the JSON file as a guide

    Parameters:
        chart: dict
            One single chart from the JSON dict
        output_dir: Path
            Folder were song art will be downloaded
        cancel_event: Event
            To check cancelation of the process

    """

    image_url = chart["song"]["imagePath"]
    filename = Path(image_url).name

    output_path = output_dir / filename

    # Check if file already is in cache
    if output_path.exists():
        return

    try:

        response = _session.get(image_url, timeout=10)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)

        return True

    except requests.RequestException as e:
        print(f"Failed: {image_url} -> {e}")
        return False


def delete_cache():
    """
    Deletes saved cache in cache folder
    """

    output_dir = APPCACHE_DIR

    for songcard in output_dir.iterdir():
        if songcard.name.endswith(".png") or songcard.name.endswith(".cache"):
            songcard.unlink()


class CacheWorker(QObject):
    progress = Signal(int)
    finished = Signal()
    error = Signal(str)
    status = Signal(int, int)

    def __init__(self, json_file):
        super().__init__()
        self.json_file = json_file

    def run(self):
        try:
            charts = load_json(self.json_file)
            output_dir = APPCACHE_DIR
            output_dir.parent.mkdir(parents=True, exist_ok=True)

            results = charts["results"]
            total = len(results)
            completed = 0
            cancelled = False

            with ThreadPoolExecutor(max_workers=15) as executor:
                futures = {
                    executor.submit(
                        download_image, chart, output_dir
                    ): chart
                    for chart in results
                }

                pending = set(futures.keys())

                while pending and not cancelled:

                    # Wait up to 0.2s for any future to complete
                    done, pending = wait(
                        pending, timeout=0.2,
                        return_when=FIRST_COMPLETED
                    )

                    for future in done:
                        try:
                            future.result()
                        except Exception as e:
                            print(f"Worker error: {e}")
                        completed += 1

                    if completed:
                        progress = int(completed / total * 100)
                        self.status.emit(completed, total)
                        self.progress.emit(progress)

            (APPCACHE_DIR/".cache").touch()
            self.finished.emit()

        except Exception as e:
            print(f"Download Failed: {e}")
            self.error.emit(str(e))
