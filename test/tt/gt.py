#!/data/data/com.termux/files/usr/bin/env python3
# gt_trends24.py - Regional & Category Trending Hashtag Scraper + Git Push

import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import time
import os
import subprocess
import logging
import random

# ---------------- CONFIG ----------------
UPDATE_INTERVAL = 30 * 60
BASE_DIR = os.path.expanduser("~/scripts")

TRENDS_FILE = os.path.join(BASE_DIR, "trends.txt")
TOP_N = 15
GIT_REPO = BASE_DIR

HEADERS = {"User-Agent": "Mozilla/5.0"}
REQUEST_TIMEOUT = 10

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ---------------- REGIONS ----------------
REGIONS = {
    "1": ("Global", "https://trends24.in/"),
    "2": ("USA", "https://trends24.in/united-states/"),
    "3": ("UK", "https://trends24.in/united-kingdom/"),
    "4": ("India", "https://trends24.in/india/"),
    "5": ("Germany", "https://trends24.in/germany/"),
    "6": ("Japan", "https://trends24.in/japan/"),
}

# ---------------- CATEGORY ----------------
CATEGORIES = {
    "1": "General",
    "2": "Sports",
    "3": "Entertainment",
    "4": "Politics"
}

# ---------------- INPUT ----------------
def choose_category():
    print("\nSelect category (optional, press Enter to skip, default: General):")
    for k, v in CATEGORIES.items():
        print(f"{k}. {v}")
    choice = input("Enter category number or skip: ").strip()
    return CATEGORIES.get(choice, "General")

def choose_regions():
    print("\nSelect regions (comma separated, default: Global):")
    for k, v in REGIONS.items():
        print(f"{k}. {v[0]}")
    choice = input("Enter region numbers: ").split(",")
    valid = [c.strip() for c in choice if c.strip() in REGIONS]
    if not valid:
        valid = ["1"]
    return [REGIONS[v] for v in valid]

# ---------------- FETCH ----------------
def fetch(url):
    try:
        time.sleep(random.uniform(1,2))
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except Exception as e:
        logging.warning(f"Failed to fetch {url}: {e}")
        return None

# ---------------- SCRAPE ----------------
def scrape_trends24(url):
    html = fetch(url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    tags = []
    for a in soup.select("a"):
        t = a.get_text(strip=True)
        if t.startswith("#"):
            clean = re.sub(r"[^\w#]", "", t)
            if re.match(r"^#[A-Za-z0-9_]{2,50}$", clean):
                tags.append(clean)
    return tags

# ---------------- SCORE ----------------
def score_tag(tag):
    score = max(0, 25 - len(tag))
    if any(x in tag.lower() for x in ["fc","vs","cup","match","game"]):
        score += 10
    return score

def process_tags(tags):
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
    logging.info(f"Saved {len(data)} trends to {path}")

# ---------------- GIT ----------------
def git_push():
    try:
        if subprocess.run(["git","-C",GIT_REPO,"diff","--quiet"]).returncode == 0:
            logging.info("No changes to commit")
            return
        subprocess.run(["git","-C",GIT_REPO,"add","."], check=True)
        subprocess.run(["git","-C",GIT_REPO,"commit","-m","trends update"], check=True)
        subprocess.run(["git","-C",GIT_REPO,"push"], check=True)
        logging.info("Git push complete")
    except Exception as e:
        logging.error(f"Git push failed: {e}")

# ---------------- MAIN ----------------
def main():
    logging.info("Starting Trends24 Trend Scraper...")
    category = choose_category()
    regions = choose_regions()
    logging.info(f"Category: {category}, Regions: {[r[0] for r in regions]}")

    while True:
        all_tags = []
        for name, url in regions:
            tags = scrape_trends24(url)
            if tags:
                all_tags.extend(tags)

        if not all_tags:
            logging.warning("No trends scraped")
        else:
            processed = process_tags(all_tags)
            save_list(TRENDS_FILE, processed)
            git_push()

        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
