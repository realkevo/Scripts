#!/data/data/com.termux/files/usr/bin/env python3
# gt.py - Global Trending Hashtag Scraper with Guaranteed Git Push
# Scrapes hashtags, saves to trends.txt and pushes to GitHub every 30 minutes

import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import time
import os
import random
import subprocess

# ---------------- CONFIG ----------------
UPDATE_INTERVAL = 30 * 60  # 30 minutes
TRENDS_FILE = os.path.expanduser("~/scripts/trends.txt")
TREND_SITES = [
    "https://trends24.in/",
]
HEADERS = {"User-Agent": "Mozilla/5.0"}
TOP_N = 20
GIT_REPO = os.path.expanduser("~/scripts")
# ----------------------------------------

def scrape_trends():
    """Scrape hashtags"""
    all_tags = []

    for url in TREND_SITES:
        try:
            r = requests.get(url, headers=HEADERS)
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.text, "html.parser")

            for a in soup.find_all("a"):
                text = a.text.strip()

                if text.startswith("#"):
                    clean = re.sub(r"[^\w#]", "", text)

                    if re.match(r"^#[A-Za-z0-9_]{2,50}$", clean):
                        all_tags.append(clean)

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    ranked = [tag for tag, _ in Counter(all_tags).most_common(TOP_N*2)]
    return ranked


def save_rotated(tags):
    """Save hashtags and force file change"""
    rotated = random.sample(tags, min(TOP_N, len(tags))) if tags else []

    with open(TRENDS_FILE, "w") as f:
        for tag in rotated:
            f.write(tag + " ")

        # Force change so git always commits
        f.write("\n# update " + time.strftime("%Y-%m-%d %H:%M:%S"))

    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] trends.txt updated")


def git_commit_push():
    """Always commit and push"""
    try:

        subprocess.run(["git", "-C", GIT_REPO, "add", "trends.txt"])

        msg = f"Update trends {time.strftime('%Y-%m-%d %H:%M:%S')}"

        subprocess.run(["git", "-C", GIT_REPO, "commit", "-m", msg])

        subprocess.run(["git", "-C", GIT_REPO, "push", "origin", "main"])

        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] pushed to GitHub")

    except Exception as e:
        print("Git error:", e)


def main():

    print("GT.py started")

    while True:

        tags = scrape_trends()

        if tags:
            save_rotated(tags)
        else:
            print("No hashtags scraped")

        git_commit_push()

        print("Sleeping 30 minutes...\n")

        time.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    main()
