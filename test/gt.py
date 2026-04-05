#!/data/data/com.termux/files/usr/bin/env python3
# gt_elite.py - Trend Intelligence Engine (Scored + Categorized + API + Git)

import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import time
import os
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

TOP_N = 15
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

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ------------------------ REGION SETUP --------------------------
def choose_regions():
    if os.path.exists(REGION_FILE):
        with open(REGION_FILE, "r") as f:
            saved = f.read().strip().split(",")
            if saved:
                return [REGIONS[k][1] for k in saved if k in REGIONS]

    print("\nSelect regions (comma separated):\n")
    for key, (name, _) in REGIONS.items():
        print(f"{key}. {name}")

    choices = input("\nEnter: ").split(",")
    valid = [c.strip() for c in choices if c.strip() in REGIONS]

    if not valid:
        valid = ["1"]

    with open(REGION_FILE, "w") as f:
        f.write(",".join(valid))

    return [REGIONS[v][1] for v in valid]

# ------------------------ FETCH ------------------------------
def fetch_url(url):
    for _ in range(MAX_RETRIES):
        try:
            r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            r.encoding = "utf-8"
            return r.text
        except:
            time.sleep(2)
    return None

# ------------------------ SCRAPE ------------------------------
def scrape_trends(url):
    html = fetch_url(url)
    tags = []

    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")

    for a in soup.select("a"):
        t = a.get_text(strip=True)
        if t.startswith("#"):
            clean = re.sub(r"[^\w#]", "", t)
            if re.match(r"^#[A-Za-z0-9_]{2,50}$", clean):
                tags.append(clean)

    return tags

# ------------------------ CATEGORY ---------------------------
def categorize(tag):
    t = tag.lower()

    if any(x in t for x in ["fc", "vs", "league", "match", "championship"]):
        return "sports"
    if any(x in t for x in ["news", "live", "breaking"]):
        return "news"
    if any(x in t for x in ["show", "music", "tv", "spotify"]):
        return "entertainment"

    return "general"

# ------------------------ SCORING -----------------------------
def score_tag(tag):
    blacklist = ["fancon", "kpop", "bts", "enhypen", "vote", "stream"]

    t = tag.lower()

    if any(b in t for b in blacklist):
        return -100

    score = 0

    score += max(0, 30 - len(tag))

    if tag.isupper():
        score += 5

    if any(x in t for x in ["fc", "vs", "live", "news", "championship"]):
        score += 15

    return score

# ------------------------ AGGREGATE ---------------------------
def aggregate(urls):
    combined = []
    for u in urls:
        combined.extend(scrape_trends(u))

    counts = Counter(combined)

    scored = []
    for tag, freq in counts.items():
        s = score_tag(tag)
        if s > 0:
            total_score = s + freq * 5
            scored.append((tag, total_score, categorize(tag)))

    scored.sort(key=lambda x: x[1], reverse=True)

    return scored[:TOP_N]

# ------------------------ STORAGE -----------------------------
def load_previous():
    if not os.path.exists(TRENDS_JSON):
        return []
    try:
        with open(TRENDS_JSON) as f:
            return json.load(f).get("trends", [])
    except:
        return []

def save_trends(data):
    try:
        tags_only = [t["tag"] for t in data]

        with open(TRENDS_FILE, "w") as f:
            f.write("\n".join(tags_only))

        with open(TRENDS_JSON, "w") as f:
            json.dump({
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "trends": data
            }, f, indent=2)

        return tags_only
    except Exception as e:
        logging.error(e)
        return []

# ------------------------ GIT -----------------------------
def git_push():
    try:
        diff = subprocess.run(["git", "-C", GIT_REPO, "diff", "--quiet"])
        if diff.returncode == 0:
            return

        subprocess.run(["git", "-C", GIT_REPO, "add", "."], check=True)
        subprocess.run(["git", "-C", GIT_REPO, "commit", "-m", "auto trends"], check=True)
        subprocess.run(["git", "-C", GIT_REPO, "push"], check=True)
    except Exception as e:
        logging.error(e)

# ------------------------ API -----------------------------
class Handler(BaseHTTPRequestHandler):
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
    server = HTTPServer(("0.0.0.0", API_PORT), Handler)
    server.serve_forever()

# ------------------------ MAIN -----------------------------
def main():
    urls = choose_regions()

    if ENABLE_API:
        threading.Thread(target=start_api, daemon=True).start()

    while True:
        try:
            ranked = aggregate(urls)

            formatted = [
                {"tag": t[0], "score": t[1], "category": t[2]}
                for t in ranked
            ]

            prev = load_previous()
            curr = save_trends(formatted)

            if curr != prev:
                git_push()

        except Exception as e:
            logging.error(e)

        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
