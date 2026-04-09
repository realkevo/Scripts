<div align="center">

<h1 style="margin-bottom:0;">Trends24 Regional Hashtag Scraper</h1>
<p style="margin-top:5px; font-size:16px;">
A Python script that scrapes trending hashtags from Trends24, filters them by region and category, ranks them using a custom scoring algorithm, and automatically pushes updates to a Git repository.
</p>

</div>

<hr>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Overview</h2>

<p>
This project provides an automated solution for collecting and maintaining up-to-date trending hashtags from <strong>Trends24</strong>. The script supports multiple regions and category-based prioritization, saving the results to text and JSON files and synchronizing them with a Git repository. It is optimized for use in <strong>Termux</strong> but works on any standard Linux environment.
</p>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Key Features</h2>

<ul>
  <li><strong>Multi-Region Support:</strong> Scrape trends from Global, USA, UK, India, Germany, and Japan.</li>
  <li><strong>Category-Based Filtering:</strong> Prioritize hashtags related to Sports, Entertainment, Politics, and Technology.</li>
  <li><strong>Custom Scoring Algorithm:</strong> Combines hashtag length, frequency, and keyword relevance.</li>
  <li><strong>Automated Updates:</strong> Runs continuously and refreshes trends every 30 minutes.</li>
  <li><strong>Watchdog Monitoring:</strong> Ensures the scraper is always running using a watchdog script.</li>
  <li><strong>Git Integration:</strong> Automatically commits and pushes updates to a repository.</li>
  <li><strong>Clipboard Support:</strong> Copies the latest trends to the Termux clipboard.</li>
  <li><strong>Robust Error Handling:</strong> Includes logging, randomized delays, and request timeouts.</li>
</ul>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Project Structure</h2>

<pre>
.
├── scraper.py          # Main Trends24 scraping script
├── autopush.sh         # Automatically commits and pushes updates to GitHub
├── watch_gt.sh         # Watchdog script to keep scraper.py running
├── trends.txt          # Generated list of top hashtags
├── trends.json         # JSON formatted trends
├── x_trends.txt        # Optional X/Twitter formatted trends
├── regions.conf        # Region configuration
├── gt_watch.log        # Watchdog log file
├── gt.log              # Scraper runtime log
└── README.md           # Project documentation
</pre>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Requirements</h2>

<h3>Python Dependencies</h3>

<pre><code>pip install requests beautifulsoup4
</code></pre>

<h3>System Dependencies</h3>

<ul>
  <li>Python 3.7 or later</li>
  <li>Git</li>
  <li>Termux API (optional, for clipboard functionality)</li>
</ul>

<h3>Termux Setup</h3>

<pre><code>pkg update && pkg upgrade
pkg install python git termux-api
pip install requests beautifulsoup4
termux-setup-storage
</code></pre>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Configuration</h2>

<p>The following constants can be adjusted within the script:</p>

<table>
  <thead>
    <tr>
      <th>Variable</th>
      <th>Description</th>
      <th>Default Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>UPDATE_INTERVAL</code></td>
      <td>Time between updates</td>
      <td>30 minutes</td>
    </tr>
    <tr>
      <td><code>BASE_DIR</code></td>
      <td>Directory for saving output</td>
      <td><code>~/scripts</code></td>
    </tr>
    <tr>
      <td><code>TRENDS_FILE</code></td>
      <td>Output file path</td>
      <td><code>~/scripts/trends.txt</code></td>
    </tr>
    <tr>
      <td><code>TOP_N</code></td>
      <td>Number of top hashtags</td>
      <td>15</td>
    </tr>
    <tr>
      <td><code>REQUEST_TIMEOUT</code></td>
      <td>HTTP request timeout</td>
      <td>10 seconds</td>
    </tr>
  </tbody>
</table>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Supported Regions</h2>

<!-- (Table remains unchanged) -->

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Supported Categories</h2>

<!-- (Table remains unchanged) -->

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Usage</h2>

<h3>1. Clone the Repository</h3>

<pre><code>git clone https://github.com/your-username/trends24-scraper.git
cd trends24-scraper
</code></pre>

<h3>2. Install Dependencies</h3>

<pre><code>pip install requests beautifulsoup4
</code></pre>

<h3>3. Run the Scraper</h3>

<pre><code>python3 scraper.py
</code></pre>

<p>
During execution, you will be prompted to select a category and one or more regions. The script will then run continuously, updating the trends at the configured interval.
</p>

<h3>4. Start the Watchdog (Optional)</h3>

<pre><code>chmod +x watch_gt.sh
nohup ./watch_gt.sh &
</code></pre>

<h3>5. Enable Automatic Git Push (Optional)</h3>

<pre><code>chmod +x autopush.sh
./autopush.sh
</code></pre>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Example Output</h2>

<pre>
#AI
#WorldCup
#BreakingNews
#TechNews
#MovieNight
#Election2026
</pre>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Git Integration</h2>

<p>
The <code>autopush.sh</code> script automatically stages, commits, and pushes updates to the configured Git repository. Ensure Git is properly configured before running:
</p>

<pre><code>git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
</code></pre>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Automation with Cron</h2>

<p>
You can schedule the watchdog or scraper using cron:
</p>

<pre><code>crontab -e
@reboot /data/data/com.termux/files/usr/bin/sh ~/scripts/watch_gt.sh
</code></pre>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Logging</h2>

<p>
Logging is enabled by default and provides detailed runtime information:
</p>

<ul>
  <li><code>gt.log</code> – Scraper runtime logs</li>
  <li><code>gt_watch.log</code> – Watchdog activity logs</li>
</ul>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Disclaimer</h2>

<p>
This project is intended for educational and research purposes. Users should ensure compliance with the terms of service of Trends24. The script includes delays and respectful scraping practices to minimize server load.
</p>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Contributing</h2>

<p>
Contributions are welcome. Please feel free to open issues or submit pull requests to enhance the functionality of this project.
</p>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">License</h2>

<p>
This project is licensed under the MIT License. See the <code>LICENSE</code> file for more information.
</p>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:5px;">Author</h2>

<p>
<strong>Kelvin</strong><br>
Developer and software engineer focused on automation and AI-driven solutions.
</p>
