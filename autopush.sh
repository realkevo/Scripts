#!/data/data/com.termux/files/usr/bin/sh
cd ~/scripts || exit

git add scraper.py
git commit -m "Auto-update scraper.py"
git push origin main
