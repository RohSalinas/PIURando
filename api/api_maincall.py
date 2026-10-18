import requests
import json
from pathlib import Path
import base64
import os

from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from PySide6.QtCore import QObject, Signal
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


LOCAL_APP_DATA = Path(
    os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")
)

BASE_URL = "https://piuscores.arroweclip.se"

APPCACHE_DIR = LOCAL_APP_DATA / "PIURando" / "appcache"
SONGS_DIR = APPCACHE_DIR / "songcards"
TOKEN_PATH = APPCACHE_DIR / "token.txt"


def get_token():
    if not TOKEN_PATH.exists():
        return None

    return TOKEN_PATH.read_text(encoding="utf-8").strip()


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


def get_charts_info_v2(mix=None, chart_type=None, level=None, count=False, max_count=4, status_callback=None):
    """
    Fetch charts from /api/charts with optional filters and save a dump JSON file.

    Parameters:
        mix        : Game version string, e.g. "Phoenix", "XX", "Fiesta2"
        chart_type : "Single" or "Double"
        level      : int (1 to 29)
        count      : Max number of charts to fetch from the API
    """

    APPCACHE_DIR.mkdir(parents=True, exist_ok=True)
    SONGS_DIR.mkdir(parents=True, exist_ok=True)

    TOKEN = get_token()
    basic = base64.b64encode(f":{TOKEN}".encode()).decode()
    HEADERS = {
        "Authorization": f"Basic {basic}",
        "Accept": "*/*",
    }

    params = {
        "mix": mix,
        "limit": 500,
    }

    if chart_type:
        params["type"] = chart_type

    all_results = []
    url = f"{BASE_URL}/api/v2/charts"

    print(params)

    while url:

        if status_callback:
            status_callback(
                f"Retrieving chart data... {len(all_results)} / {data['total']}")

        try:
            response = _session.get(
                url,
                headers=HEADERS,
                params=params,
                timeout=10,
            )

        except requests.ConnectionError:
            print("Could not connect to the remote server.")

            return None

        except requests.Timeout:
            print("The remote server took too long to respond.")
            return None

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

        print(f"Status : {response.status_code}")
        print(f"URL    : {response.url}\n")

        if not response.ok:
            print("STATUS:", response.status_code)
            print("RESPONSE:", response.text)
            return None

        data = response.json()
        all_results.extend(data["data"])

        print(
            f"Downloaded {len(all_results)} / {data['total']}"
        )

        url = data.get("next")
        params = None

    output = {
        "data": all_results,
        "total": len(all_results),
    }

    output_file = APPCACHE_DIR / "dump_all_v2.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    return output


def load_json(file_path):
    """
    Load JSON files

    Parameteres:
        file_path: Path
            JSON dump file path

    Returns:
        JSON file as a python dict    
    """

    with open(file_path, encoding="utf-8") as f:
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

    image_url = chart["imageUrl"]
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


def delete_cache(apidialog):
    """
    Deletes saved cache in cache folder
    """

    for songcard in SONGS_DIR.iterdir():
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
            output_dir = SONGS_DIR
            output_dir.mkdir(parents=True, exist_ok=True)

            # results = charts["results"]
            results = charts["data"]
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

            (SONGS_DIR / ".cache").touch()
            self.finished.emit()

        except Exception as e:
            print(f"Download Failed: {e}")
            self.error.emit(str(e))
