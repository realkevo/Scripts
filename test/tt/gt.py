#!/data/data/com.termux/files/usr/bin/env python3
# gt_dual_source.py - Dual Source Trend Engine (Twitter + Trends24)

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
import random

# ---------------- CONFIG ----------------
UPDATE_INTERVAL = 30 * 60
BASE_DIR = os.path.expanduser("~/scripts")

TWITTER_FILE = os.path.join(BASE_DIR, "twitter.txt")
TRENDS_FILE = os.path.join(BASE_DIR, "trends.txt")
TRENDS_JSON = os.path.join(BASE_DIR, "trends.json")

TOP_N = 15
GIT_REPO = BASE_DIR

HEADERS = {"User-Agent": "Mozilla/5.0"}
REQUEST_TIMEOUT = 10

ENABLE_API = True
API_PORT = 8000

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ---------------- REGIONS ----------------
REGIONS = {
    "1": ("Global", "https://trends24.in/", 1),
    "2": ("USA", "https://trends24.in/united-states/", 23424977),
    "3": ("UK", "https://trends24.in/united-kingdom/", 23424975),
}

# ---------------- INPUT ----------------
def choose_regions():
    print("\nSelect regions (comma separated):")
    for k, v in REGIONS.items():
        print(f"{k}. {v[0]}")

    choice = input("Enter: ").split(",")
    valid = [c.strip() for c in choice if c.strip() in REGIONS]

    if not valid:
        valid = ["1"]

    return [REGIONS[v] for v in valid]

# ---------------- FETCH ----------------
def fetch(url, headers=None):
    try:
        time.sleep(random.uniform(1,2))
        r = requests.get(url, headers=headers or HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r
    except:
        return None

# ---------------- TWITTER ----------------
def get_guest_token():
    r = fetch("https://twitter.com/")
    if not r:
        return None
    match = re.search(r'gt=(\d+);', r.text)
    return match.group(1) if match else None

def scrape_twitter(woeid):
    token = get_guest_token()
    if not token:
        return []

    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAA",
        "x-guest-token": token,
        "User-Agent": "Mozilla/5.0"
    }

    url = f"https://twitter.com/i/api/1.1/trends/place.json?id={woeid}"
    r = fetch(url, headers=headers)
    if not r:
        return []

    try:
        data = r.json()
        return [t["name"] for t in data[0]["trends"] if t["name"].startswith("#")]
    except:
        return []

# ---------------- TRENDS24 ----------------
def scrape_trends24(url):
    r = fetch(url)
    if not r:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    tags = []

    for a in soup.select("a"):
        t = a.get_text(strip=True)
        if t.startswith("#"):
            clean = re.sub(r"[^\w#]", "", t)
            tags.append(clean)

    return tags

# ---------------- SCORE ----------------
def score_tag(tag):
    score = max(0, 25 - len(tag))
    if any(x in tag.lower() for x in ["fc","vs","cup"]):
        score += 10
    return score

# ---------------- PROCESS ----------------
def process(tags):
    counts = Counter(tags)
    scored = []

    for tag, freq in counts.items():
        s = score_tag(tag)
        if s > 0:
            scored.append((tag, s + freq*5))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [t[0] for t in scored[:TOP_N]]

# ---------------- SAVE ----------------
def save_list(path, data):
    with open(path, "w") as f:
        f.write("\n".join(data))

# ---------------- GIT ----------------
def git_push():
    try:
        if subprocess.run(["git","-C",GIT_REPO,"diff","--quiet"]).returncode == 0:
            return

        subprocess.run(["git","-C",GIT_REPO,"add","."], check=True)
        subprocess.run(["git","-C",GIT_REPO,"commit","-m","dual source trends"], check=True)
        subprocess.run(["git","-C",GIT_REPO,"push"], check=True)

        logging.info("Git push complete")
    except Exception as e:
        logging.error(e)

# ---------------- MAIN ----------------
def main():
    logging.info("Starting dual-source engine...")

    regions = choose_regions()

    while True:
        try:
            twitter_tags = []
            trends_tags = []

            # ---- TWITTER FIRST ----
            for name, url, woeid in regions:
                twitter_tags.extend(scrape_twitter(woeid))

            if twitter_tags:
                processed_twitter = process(twitter_tags)
                save_list(TWITTER_FILE, processed_twitter)
                logging.info(f"Saved Twitter trends ({len(processed_twitter)})")

            else:
                logging.warning("Twitter scrape failed")

            # ---- ALWAYS RUN TRENDS24 ----
            for name, url, woeid in regions:
                trends_tags.extend(scrape_trends24(url))

            if trends_tags:
                processed_trends = process(trends_tags)
                save_list(TRENDS_FILE, processed_trends)
                logging.info(f"Saved Trends24 trends ({len(processed_trends)})")

            # ---- PUSH BOTH ----
            git_push()

        except Exception as e:
            logging.error(e)

        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
