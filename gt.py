#!/data/data/com.termux/files/usr/bin/env python3
# gt.py - Global Trending Hashtag Scraper with Auto Git Push
# Scrapes global hashtags, rotates top 20, saves to trends.txt, and pushes to GitHub

import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import time
import os
import random
import subprocess  # for running git commands

# ---------------------------- CONFIG ----------------------------
UPDATE_INTERVAL = 30 * 60  # scrape every 30 minutes
TRENDS_FILE = os.path.expanduser("~/scripts/trends.txt")  # output file
TREND_SITES = [
    "https://trends24.in/",  # Global trends
]
HEADERS = {"User-Agent": "Mozilla/5.0"}
TOP_N = 20  # number of hashtags to rotate and save
GIT_REPO = os.path.expanduser("~/scripts")  # local git repo path
# ---------------------------------------------------------------

def scrape_trends():
    """Scrape hashtags from TREND_SITES and return top hashtags list"""
    all_tags = []

    for url in TREND_SITES:
        try:
            r = requests.get(url, headers=HEADERS)
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.text, "html.parser")

            # Find all <a> tags and extract hashtags
            for a in soup.find_all("a"):
                text = a.text.strip()
                if text.startswith("#"):
                    # Remove any unwanted characters except #, letters, numbers, _
                    clean = re.sub(r"[^\w#]", "", text)
                    # Only consider reasonable hashtags
                    if re.match(r"^#[A-Za-z0-9_]{2,50}$", clean):
                        all_tags.append(clean)

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    # Count frequency and rank hashtags
    ranked = [tag for tag, _ in Counter(all_tags).most_common(TOP_N*2)]
    return ranked

def save_rotated(tags, n=TOP_N):
    """Randomly select n hashtags from scraped list and save to TRENDS_FILE"""
    rotated = random.sample(tags, min(n, len(tags))) if tags else []
    with open(TRENDS_FILE, "w") as f:
        for tag in rotated:
            f.write(tag + " ")
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Saved {len(rotated)} hashtags to {TRENDS_FILE}")
    return rotated

def git_commit_push(file_path, repo_path):
    """Automatically commit and push trends.txt to GitHub"""
    try:
        subprocess.run(["git", "-C", repo_path, "add", file_path], check=True)
        commit_msg = f"Auto-update trends: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "-C", repo_path, "push", "origin", "main"], check=True)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] trends.txt pushed to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"Git push failed: {e}")

def main():
    """Main loop: scrape, save, git push, then wait UPDATE_INTERVAL"""
    while True:
        tags = scrape_trends()
        if tags:
            save_rotated(tags)
            git_commit_push("trends.txt", GIT_REPO)
        else:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] No hashtags found")
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
