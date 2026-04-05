#!/data/data/com.termux/files/usr/bin/env bash
# Watchdog for gt.py - ensures it always runs (checks every 30 minutes)

SCRIPT="$HOME/scripts/gt.py"
LOG="$HOME/scripts/gt_watch.log"

# Prevent Termux from sleeping
termux-wake-lock

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Watchdog started" >> "$LOG"

while true; do
    # Check if gt.py is running
    if ! pgrep -f "$SCRIPT" > /dev/null; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] gt.py not running, starting..." >> "$LOG"
        nohup python3 "$SCRIPT" >> "$LOG" 2>&1 &
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] gt.py started" >> "$LOG"
    fi
    sleep 1800  # wait 30 minutes before next check
done
