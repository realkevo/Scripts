#!/data/data/com.termux/files/usr/bin/env python3
# gt_trends24_upgraded.py
#
# Regional & Category Trending Hashtag Scraper + Git Push
#
# TOP-LEVEL CATEGORIES:
# 1. General
# 2. Sports
# 3. Entertainment
# 4. Politics
# 5. Technology
# 6. Eye Users
# 7. X
#
# X SUBCATEGORIES:
# 1. General X Trends
# 2. Sports
# 3. Entertainment
# 4. Politics
# 5. Technology
# 6. AI
# 7. Photography & Images
# 8. Android & Apps
# 9. Gaming
# 10. Business & Finance
# 11. News
# 12. Viral / Meme
# 13. Creators & Social Media
# 14. Eye Users
#
# Existing functionality preserved:
# - Trends24 scraping
# - Multiple regions
# - 30-minute updates
# - Top 15 trends
# - trends.txt output
# - Termux clipboard
# - Automatic Git push


import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import time
import os
import subprocess
import logging
import random


# ============================================================
# CONFIG
# ============================================================

UPDATE_INTERVAL = 30 * 60  # 30 minutes

BASE_DIR = os.path.expanduser("~/scripts")

TRENDS_FILE = os.path.join(BASE_DIR, "trends.txt")

TOP_N = 15

GIT_REPO = BASE_DIR

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

REQUEST_TIMEOUT = 10


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


# ============================================================
# REGIONS
# ============================================================

REGIONS = {
    "1": ("Global", "https://trends24.in/"),
    "2": ("USA", "https://trends24.in/united-states/"),
    "3": ("UK", "https://trends24.in/united-kingdom/"),
    "4": ("India", "https://trends24.in/india/"),
    "5": ("Germany", "https://trends24.in/germany/"),
    "6": ("Japan", "https://trends24.in/japan/"),
}


# ============================================================
# TOP-LEVEL CATEGORIES
# ============================================================

CATEGORIES = {
    "1": "General",
    "2": "Sports",
    "3": "Entertainment",
    "4": "Politics",
    "5": "Technology",
    "6": "Eye Users",
    "7": "X"
}


# ============================================================
# X SUBCATEGORIES
# ============================================================

X_CATEGORIES = {
    "1": "General X Trends",
    "2": "Sports",
    "3": "Entertainment",
    "4": "Politics",
    "5": "Technology",
    "6": "AI",
    "7": "Photography & Images",
    "8": "Android & Apps",
    "9": "Gaming",
    "10": "Business & Finance",
    "11": "News",
    "12": "Viral / Meme",
    "13": "Creators & Social Media",
    "14": "Eye Users"
}


# ============================================================
# CATEGORY KEYWORDS
# ============================================================

CATEGORY_KEYWORDS = {

    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------

    "General": [],


    # --------------------------------------------------------
    # SPORTS
    # --------------------------------------------------------

    "Sports": [
        "sport",
        "sports",
        "football",
        "soccer",
        "basketball",
        "baseball",
        "tennis",
        "cricket",
        "rugby",
        "golf",
        "boxing",
        "ufc",
        "wwe",
        "nfl",
        "nba",
        "nhl",
        "mlb",
        "fifa",
        "uefa",
        "ucl",
        "europa",
        "premierleague",
        "epl",
        "laliga",
        "seriea",
        "bundesliga",
        "ligue1",
        "championsleague",
        "worldcup",
        "superbowl",
        "formula1",
        "f1",
        "nascar",
        "race",
        "racing",
        "match",
        "game",
        "games",
        "league",
        "cup",
        "final",
        "finals",
        "semifinal",
        "playoffs",
        "transfer",
        "transfers",
        "goal",
        "goals",
        "fc",
        "vs",
        "champion",
        "champions",
        "coach",
        "manager",
        "player",
        "players",
        "team",
        "teams"
    ],


    # --------------------------------------------------------
    # ENTERTAINMENT
    # --------------------------------------------------------

    "Entertainment": [
        "entertainment",
        "movie",
        "movies",
        "film",
        "films",
        "cinema",
        "hollywood",
        "bollywood",
        "netflix",
        "series",
        "tv",
        "television",
        "show",
        "shows",
        "episode",
        "episodes",
        "actor",
        "actress",
        "celebrity",
        "celebrities",
        "music",
        "song",
        "songs",
        "album",
        "albums",
        "concert",
        "concerts",
        "singer",
        "artist",
        "artists",
        "grammy",
        "grammys",
        "emmys",
        "oscars",
        "oscar",
        "award",
        "awards",
        "anime",
        "manga",
        "gaming",
        "games",
        "reality",
        "realitytv",
        "premiere",
        "trailer"
    ],


    # --------------------------------------------------------
    # POLITICS
    # --------------------------------------------------------

    "Politics": [
        "politics",
        "political",
        "vote",
        "voting",
        "election",
        "elections",
        "president",
        "presidential",
        "senate",
        "senator",
        "congress",
        "government",
        "minister",
        "parliament",
        "democrat",
        "republican",
        "democrats",
        "republicans",
        "campaign",
        "candidate",
        "candidates",
        "policy",
        "politician",
        "politicians",
        "whitehouse",
        "presidency",
        "law",
        "laws",
        "bill",
        "protest",
        "protests",
        "politicalnews",
        "election2026"
    ],


    # --------------------------------------------------------
    # TECHNOLOGY
    # --------------------------------------------------------

    "Technology": [
        "technology",
        "tech",
        "ai",
        "artificialintelligence",
        "machinelearning",
        "deeplearning",
        "ml",
        "software",
        "hardware",
        "computer",
        "computers",
        "android",
        "iphone",
        "ios",
        "google",
        "microsoft",
        "apple",
        "samsung",
        "openai",
        "chatgpt",
        "gemini",
        "claude",
        "robot",
        "robots",
        "robotics",
        "coding",
        "programming",
        "developer",
        "developers",
        "app",
        "apps",
        "mobile",
        "smartphone",
        "gadget",
        "gadgets",
        "internet",
        "cloud",
        "cybersecurity",
        "crypto",
        "blockchain"
    ],


    # --------------------------------------------------------
    # EYE USERS
    # --------------------------------------------------------

    "Eye Users": [

        # AI
        "ai",
        "artificialintelligence",
        "machinelearning",
        "deeplearning",
        "computervision",
        "visionai",
        "generativeai",
        "aiart",
        "aitools",
        "aitool",
        "aiphoto",
        "aiimage",
        "aiimages",

        # Images
        "image",
        "images",
        "photo",
        "photos",
        "picture",
        "pictures",
        "photography",
        "photographer",
        "photographers",
        "photograph",
        "visual",
        "visuals",

        # Image search
        "imagesearch",
        "reversesearch",
        "reverseimagesearch",
        "visualsearch",
        "searchbyimage",
        "searchimage",

        # Photo management
        "photogallery",
        "gallery",
        "photoalbum",
        "photoalbums",
        "imagegallery",
        "photoorganization",
        "photoorganizer",
        "photomanagement",
        "imagemanagement",
        "filemanagement",
        "media",

        # Editing
        "photoediting",
        "photoeditor",
        "imageediting",
        "imageeditor",
        "photoedit",
        "imageedit",
        "retouching",
        "photoshop",
        "lightroom",

        # Creators
        "digitalart",
        "digitalartist",
        "artist",
        "artists",
        "creator",
        "creators",
        "contentcreator",
        "contentcreators",
        "design",
        "designer",
        "graphicdesign",
        "illustration",
        "illustrator",

        # Android
        "android",
        "androidapps",
        "androidapp",
        "mobileapp",
        "mobileapps",
        "smartphone",
        "phone",
        "app",
        "apps",

        # Privacy / offline AI
        "privacy",
        "privacymatters",
        "offline",
        "offlineai",
        "localai",
        "ondeviceai",
        "ondevice",
        "dataprivacy",

        # Recognition
        "objectdetection",
        "imagerecognition",
        "facerecognition",
        "ocr",
        "textrecognition",
        "visualrecognition",
        "patternrecognition",

        # Photography
        "phototips",
        "photographytips",
        "photooftheday",
        "picoftheday",
        "photooftheweek",
        "streetphotography",
        "mobilephotography",
        "iphonephotography",
        "androidphotography",
        "naturephotography",
        "portraitphotography",
        "travelphotography",

        # General
        "content",
        "digital",
        "technology",
        "tech"
    ],


    # ========================================================
    # X SUBCATEGORIES
    # ========================================================

    "General X Trends": [],


    "AI": [
        "ai",
        "artificialintelligence",
        "machinelearning",
        "deeplearning",
        "generativeai",
        "aiart",
        "aitools",
        "aitool",
        "openai",
        "chatgpt",
        "gemini",
        "claude",
        "midjourney",
        "llm",
        "robot",
        "robotics",
        "computer",
        "computervision",
        "imagegeneration",
        "aiimage",
        "aiimages"
    ],


    "Photography & Images": [
        "photography",
        "photo",
        "photos",
        "photographer",
        "photographers",
        "picture",
        "pictures",
        "image",
        "images",
        "visual",
        "visuals",
        "photooftheday",
        "picoftheday",
        "streetphotography",
        "mobilephotography",
        "naturephotography",
        "portraitphotography",
        "travelphotography",
        "photoediting",
        "photoeditor",
        "imageediting",
        "imageeditor",
        "digitalart",
        "graphicdesign",
        "illustration"
    ],


    "Android & Apps": [
        "android",
        "androidapp",
        "androidapps",
        "googleplay",
        "playstore",
        "app",
        "apps",
        "mobileapp",
        "mobileapps",
        "smartphone",
        "phone",
        "iphone",
        "ios",
        "developer",
        "developers",
        "kotlin",
        "flutter",
        "technology",
        "tech"
    ],


    "Gaming": [
        "gaming",
        "gamer",
        "gamers",
        "game",
        "games",
        "videogame",
        "videogames",
        "playstation",
        "xbox",
        "nintendo",
        "steam",
        "esports",
        "esport",
        "fortnite",
        "minecraft",
        "roblox",
        "gta",
        "cod",
        "callofduty",
        "valorant",
        "leagueoflegends"
    ],


    "Business & Finance": [
        "business",
        "finance",
        "money",
        "investing",
        "investment",
        "investor",
        "investors",
        "stocks",
        "stockmarket",
        "market",
        "markets",
        "economy",
        "economics",
        "trading",
        "crypto",
        "bitcoin",
        "ethereum",
        "startup",
        "startups",
        "entrepreneur",
        "entrepreneurship",
        "fintech"
    ],


    "News": [
        "news",
        "breakingnews",
        "breaking",
        "latest",
        "update",
        "updates",
        "worldnews",
        "newsupdate",
        "headline",
        "headlines",
        "report",
        "reports",
        "journalism",
        "media"
    ],


    "Viral / Meme": [
        "viral",
        "trending",
        "trend",
        "meme",
        "memes",
        "funny",
        "lol",
        "comedy",
        "humor",
        "internet",
        "fyp",
        "viralvideo",
        "reaction",
        "reactions",
        "wtf",
        "wow"
    ],


    "Creators & Social Media": [
        "creator",
        "creators",
        "contentcreator",
        "contentcreators",
        "influencer",
        "influencers",
        "socialmedia",
        "youtube",
        "tiktok",
        "instagram",
        "facebook",
        "streamer",
        "streamers",
        "podcast",
        "podcasts",
        "blogger",
        "bloggers",
        "digitalcreator",
        "community"
    ]
}


# ============================================================
# INPUT - X SUBCATEGORY
# ============================================================

def choose_x_category():

    print("\nSelect X category:")

    for k, v in X_CATEGORIES.items():
        print(f"{k}. {v}")

    choice = input(
        "Enter X category number "
        "(default: General X Trends): "
    ).strip()

    return X_CATEGORIES.get(
        choice,
        "General X Trends"
    )


# ============================================================
# INPUT - CATEGORY
# ============================================================

def choose_category():

    print(
        "\nSelect category "
        "(optional, press Enter to skip, default: General):"
    )

    for k, v in CATEGORIES.items():
        print(f"{k}. {v}")

    choice = input(
        "Enter category number or skip: "
    ).strip()

    category = CATEGORIES.get(
        choice,
        "General"
    )

    # --------------------------------------------------------
    # If X selected, ask for X subcategory
    # --------------------------------------------------------

    if category == "X":

        x_category = choose_x_category()

        return "X", x_category

    return category, None


# ============================================================
# INPUT - REGIONS
# ============================================================

def choose_regions():

    print(
        "\nSelect regions "
        "(comma separated, default: Global):"
    )

    for k, v in REGIONS.items():
        print(f"{k}. {v[0]}")

    choice = input(
        "Enter region numbers: "
    ).split(",")

    valid = [
        c.strip()
        for c in choice
        if c.strip() in REGIONS
    ]

    if not valid:
        valid = ["1"]

    return [
        REGIONS[v]
        for v in valid
    ]


# ============================================================
# FETCH
# ============================================================

def fetch(url):

    try:

        # Existing random delay preserved
        time.sleep(
            random.uniform(1, 2)
        )

        r = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        r.raise_for_status()

        r.encoding = "utf-8"

        return r.text

    except Exception as e:

        logging.warning(
            f"Failed to fetch {url}: {e}"
        )

        return None


# ============================================================
# SCRAPE
# ============================================================

def scrape_trends24(url):

    html = fetch(url)

    if not html:
        return []

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    tags = []

    for a in soup.select("a"):

        t = a.get_text(
            strip=True
        )

        if t.startswith("#"):

            clean = re.sub(
                r"[^\w#]",
                "",
                t
            )

            if re.match(
                r"^#[A-Za-z0-9_]{2,50}$",
                clean
            ):

                tags.append(clean)

    return tags


# ============================================================
# GET ACTIVE KEYWORD CATEGORY
# ============================================================

def get_keyword_category(
    category,
    x_category=None
):

    if category == "X":

        return x_category

    return category


# ============================================================
# SCORE
# ============================================================

def score_tag(
    tag,
    category="General",
    x_category=None
):

    # --------------------------------------------------------
    # Preserve original base scoring
    # --------------------------------------------------------

    score = max(
        0,
        25 - len(tag)
    )


    # --------------------------------------------------------
    # Determine actual keyword category
    # --------------------------------------------------------

    active_category = get_keyword_category(
        category,
        x_category
    )


    tag_lower = tag.lower().replace(
        "#",
        ""
    )


    keywords = CATEGORY_KEYWORDS.get(
        active_category,
        []
    )


    # --------------------------------------------------------
    # GENERAL X
    #
    # General X trends are ranked mainly using frequency.
    # --------------------------------------------------------

    if (
        category == "X"
        and active_category == "General X Trends"
    ):

        return score


    # --------------------------------------------------------
    # Category relevance
    # --------------------------------------------------------

    for kw in keywords:

        if kw in tag_lower:

            # Existing category boost
            score += 10

            # More specific matches get stronger weighting
            if len(kw) >= 10:
                score += 8

            elif len(kw) >= 6:
                score += 4

            # Eye Users gets extra relevance
            if active_category == "Eye Users":
                score += 5

            break


    return score


# ============================================================
# PROCESS TAGS
# ============================================================

def process_tags(
    tags,
    category="General",
    x_category=None
):

    counts = Counter(tags)

    scored = []

    for tag, freq in counts.items():

        s = score_tag(
            tag,
            category,
            x_category
        )


        # ----------------------------------------------------
        # For category searches, require some relevance.
        #
        # General and General X continue to accept all trends.
        # ----------------------------------------------------

        active_category = get_keyword_category(
            category,
            x_category
        )


        if active_category in (
            "General",
            "General X Trends"
        ):

            final_score = (
                s +
                freq * 5
            )

            scored.append(
                (
                    tag,
                    final_score,
                    freq
                )
            )

        else:

            # A category keyword must match.
            if s > max(
                0,
                25 - len(tag)
            ):

                final_score = (
                    s +
                    freq * 5
                )

                scored.append(
                    (
                        tag,
                        final_score,
                        freq
                    )
                )


    # --------------------------------------------------------
    # Sort:
    #
    # 1. Final score
    # 2. Frequency
    # --------------------------------------------------------

    scored.sort(
        key=lambda x: (
            x[1],
            x[2]
        ),
        reverse=True
    )


    return [
        item[0]
        for item in scored[:TOP_N]
    ]


# ============================================================
# SAVE
# ============================================================

def save_list(
    path,
    data
):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(data)
        )


    logging.info(
        f"Saved {len(data)} trends to {path}"
    )


    # --------------------------------------------------------
    # Termux clipboard
    # --------------------------------------------------------

    try:

        subprocess.run(
            [
                "termux-clipboard-set",
                "\n".join(data)
            ],
            check=True
        )

        logging.info(
            "Trends copied to Termux clipboard"
        )

    except Exception:

        logging.warning(
            "Clipboard copy failed. "
            "Make sure termux-api is installed."
        )


# ============================================================
# GIT PUSH
# ============================================================

def git_push():

    try:

        subprocess.run(
            [
                "git",
                "-C",
                GIT_REPO,
                "add",
                TRENDS_FILE
            ],
            check=True
        )


        commit_msg = (
            "Auto trends update"
        )


        result = subprocess.run(
            [
                "git",
                "-C",
                GIT_REPO,
                "commit",
                "-m",
                commit_msg
            ],
            capture_output=True,
            text=True
        )


        if (
            "nothing to commit"
            in result.stdout.lower()
        ):

            logging.info(
                "No changes detected — "
                "overwriting trends and forcing push"
            )


        subprocess.run(
            [
                "git",
                "-C",
                GIT_REPO,
                "push"
            ],
            check=True
        )


        logging.info(
            "Git push complete"
        )


    except Exception as e:

        logging.error(
            f"Git push failed: {e}"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    logging.info(
        "Starting Trends24 Trend Scraper..."
    )


    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    category, x_category = choose_category()


    # --------------------------------------------------------
    # REGIONS
    # --------------------------------------------------------

    regions = choose_regions()


    # --------------------------------------------------------
    # LOG CONFIGURATION
    # --------------------------------------------------------

    if category == "X":

        logging.info(
            f"Category: X | "
            f"X Subcategory: {x_category} | "
            f"Regions: {[r[0] for r in regions]}"
        )

    else:

        logging.info(
            f"Category: {category} | "
            f"Regions: {[r[0] for r in regions]}"
        )


    # ========================================================
    # CONTINUOUS LOOP
    # ========================================================

    while True:

        all_tags = []


        # ----------------------------------------------------
        # SCRAPE SELECTED REGIONS
        # ----------------------------------------------------

        for name, url in regions:

            logging.info(
                f"Scraping {name}: {url}"
            )


            tags = scrape_trends24(
                url
            )


            if tags:

                logging.info(
                    f"{name}: found "
                    f"{len(tags)} hashtags"
                )

                all_tags.extend(
                    tags
                )

            else:

                logging.warning(
                    f"{name}: no hashtags found"
                )


        # ----------------------------------------------------
        # PROCESS
        # ----------------------------------------------------

        if not all_tags:

            logging.warning(
                "No trends scraped"
            )

        else:

            processed = process_tags(
                all_tags,
                category,
                x_category
            )


            # ------------------------------------------------
            # SAVE
            # ------------------------------------------------

            save_list(
                TRENDS_FILE,
                processed
            )


            # ------------------------------------------------
            # GIT
            # ------------------------------------------------

            git_push()


            # ------------------------------------------------
            # DISPLAY
            # ------------------------------------------------

            logging.info(
                f"Top {len(processed)} trends: "
                f"{processed}"
            )


        # ----------------------------------------------------
        # WAIT
        # ----------------------------------------------------

        logging.info(
            f"Next update in "
            f"{UPDATE_INTERVAL // 60} minutes."
        )


        time.sleep(
            UPDATE_INTERVAL
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
