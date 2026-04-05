#!/data/data/com.termux/files/usr/bin/env python3
# gt_pro.py - Multi-Region Trending Engine + API + Git Automation

import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import time
import os
import random
import subprocess
import logging
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# ---------------------------- CONFIG ----------------------------
UPDATE_INTERVAL = 30 * 60
BASE_DIR = os.path.expanduser("~/scripts")

TRENDS_FILE = os.path.join(BASE_DIR, "trends.txt")
TRENDS_JSON = os.path.join(BASE_DIR, "trends.json")
REGION_FILE = os.path.join(BASE_DIR, "regions.conf")

TOP_N = 20
GIT_REPO = BASE_DIR

HEADERS = {"User-Agent": "Mozilla/5.0"}
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3

ENABLE_API = True
API_PORT = 8000
# ---------------------------------------------------------------

# ---------------------------- REGIONS ---------------------------
REGIONS = {
    "1": ("Global", "https://trends24.in/"),
    "2": ("USA", "https://trends24.in/united-states/"),
    "3": ("UK", "https://trends24.in/united-kingdom/"),
    "4": ("India", "https://trends24.in/india/"),
    "5": ("Germany", "https://trends24.in/germany/"),
    "6": ("Japan", "https://trends24.in/japan/"),
}
# ---------------------------------------------------------------

# ---------------------------- LOGGING ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
# ---------------------------------------------------------------


# ------------------------ REGION SETUP --------------------------
def choose_regions():
    """Select multiple regions and persist"""
    if os.path.exists(REGION_FILE):
        with open(REGION_FILE, "r") as f:
            saved = f.read().strip().split(",")
            if saved:
                return [REGIONS[k][1] for k in saved if k in REGIONS]

    print("\nSelect regions (comma separated, e.g. 1,2,3):\n")
    for key, (name, _) in REGIONS.items():
        print(f"{key}. {name}")

    choices = input("\nEnter choices: ").split(",")

    valid = [c.strip() for c in choices if c.strip() in REGIONS]

    if not valid:
        print("Invalid input. Defaulting to Global.")
        valid = ["1"]

    with open(REGION_FILE, "w") as f:
        f.write(",".join(valid))

    logging.info(f"Regions selected: {[REGIONS[v][0] for v in valid]}")
    return [REGIONS[v][1] for v in valid]


# ------------------------ FETCHING ------------------------------
def fetch_url(url):
    for attempt in range(MAX_RETRIES):
        try:
            time.sleep(random.uniform(1, 3))
            r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            r.encoding = "utf-8"
            return r.text
        except Exception as e:
            logging.warning(f"{url} attempt {attempt+1} failed: {e}")
    return None


# ------------------------ SCRAPING ------------------------------
def scrape_trends(url):
    all_tags = []
    html = fetch_url(url)

    if not html:
        return []

    try:
        soup = BeautifulSoup(html, "html.parser")

        for a in soup.select("a"):
            text = a.get_text(strip=True)

            if text.startswith("#"):
                clean = re.sub(r"[^\w#]", "", text)

                if re.match(r"^#[A-Za-z0-9_]{2,50}$", clean):
                    all_tags.append(clean)

    except Exception as e:
        logging.error(f"Parse error: {e}")

    return all_tags


# ------------------------ AGGREGATION ---------------------------
def aggregate_trends(urls):
    combined = []

    for url in urls:
        tags = scrape_trends(url)
        combined.extend(tags)

    if not combined:
        return []

    ranked = [tag for tag, _ in Counter(combined).most_common(TOP_N * 3)]
    return ranked


# ------------------------ STORAGE -------------------------------
def load_previous():
    if not os.path.exists(TRENDS_JSON):
        return []

    try:
        with open(TRENDS_JSON, "r") as f:
            return json.load(f).get("trends", [])
    except:
        return []


def save_trends(tags):
    if not tags:
        return []

    weights = [len(tags) - i for i in range(len(tags))]
    selected = list(set(random.choices(tags, weights=weights, k=min(TOP_N * 2, len(tags)))))
    final = selected[:TOP_N]

    try:
        with open(TRENDS_FILE, "w") as f:
            f.write("\n".join(final))

        with open(TRENDS_JSON, "w") as f:
            json.dump({
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "trends": final
            }, f, indent=2)

        logging.info(f"Saved {len(final)} trends")
        return final

    except Exception as e:
        logging.error(f"Save error: {e}")
        return []


# ------------------------ GIT -----------------------------------
def git_push():
    try:
        diff = subprocess.run(["git", "-C", GIT_REPO, "diff", "--quiet"])

        if diff.returncode == 0:
            logging.info("No changes to commit")
            return

        subprocess.run(["git", "-C", GIT_REPO, "add", "."], check=True)

        msg = f"Auto trends update {time.strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "-C", GIT_REPO, "commit", "-m", msg], check=True)

        subprocess.run(["git", "-C", GIT_REPO, "push"], check=True)

        logging.info("Git push complete")

    except Exception as e:
        logging.error(f"Git error: {e}")


# ------------------------ API SERVER ----------------------------
class TrendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/trends":
            try:
                with open(TRENDS_JSON) as f:
                    data = f.read()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(data.encode())

            except:
                self.send_response(500)
                self.end_headers()


def start_api():
    server = HTTPServer(("0.0.0.0", API_PORT), TrendHandler)
    logging.info(f"API running on port {API_PORT}")
    server.serve_forever()


# ------------------------ MAIN LOOP -----------------------------
def main():
    logging.info("Starting Trend Engine...")

    urls = choose_regions()

    if ENABLE_API:
        threading.Thread(target=start_api, daemon=True).start()

    while True:
        try:
            tags = aggregate_trends(urls)

            if not tags:
                logging.warning("No data scraped")
                time.sleep(UPDATE_INTERVAL)
                continue

            previous = load_previous()
            current = save_trends(tags)

            if current != previous:
                git_push()
            else:
                logging.info("No meaningful changes")

        except Exception as e:
            logging.error(f"Fatal loop error: {e}")

        time.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    main()
