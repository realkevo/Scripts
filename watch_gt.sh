#!/data/data/com.termux/files/usr/bin/sh
# Watchdog for scraper.py - ensures it is always running

SCRIPT="$HOME/scripts/scraper.py"
LOG="$HOME/scripts/gt_watch.log"

# Prevent Termux from sleeping
termux-wake-lock

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Watchdog started for scraper.py" >> "$LOG"

while true; do
    # Check if scraper.py is running
    if ! pgrep -f "$SCRIPT" > /dev/null; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] scraper.py not running. Restarting..." >> "$LOG"
        nohup python3 "$SCRIPT" >> "$LOG" 2>&1 &
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] scraper.py started." >> "$LOG"
    fi

    # Wait 30 minutes before checking again
    sleep 1800
done
