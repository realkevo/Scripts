<div align="center">
  <h1 style="margin-bottom:0;">Trends24 Regional Hashtag Scraper</h1>
  <p style="margin-top:5px; font-size:16px;">
    A Python automation tool that scrapes trending hashtags from Trends24, ranks them using a custom scoring algorithm, and automatically pushes updates to a GitHub repository.
  </p>
</div>

<hr>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Overview</h2>

<p>
The <strong>Trends24 Regional Hashtag Scraper</strong> is a Python-based automation script designed to collect and maintain up-to-date trending hashtags from <strong>Trends24</strong>. The script supports multiple regions and category-based prioritization, saves the results to a text file, copies them to the Termux clipboard, and synchronizes updates with a GitHub repository.
</p>

<p>
The project is optimized for <strong>Termux</strong> on Android but is fully compatible with Linux, macOS, and other Unix-like environments.
</p>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Key Features</h2>

<ul>
  <li><strong>Multi-Region Support:</strong> Scrape trending hashtags from Global, USA, UK, India, Germany, and Japan.</li>
  <li><strong>Category-Based Filtering:</strong> Prioritize hashtags related to Sports, Entertainment, Politics, and Technology.</li>
  <li><strong>Custom Scoring Algorithm:</strong> Ranks hashtags based on length, frequency, and category relevance.</li>
  <li><strong>Automated Updates:</strong> Continuously refreshes trends every 30 minutes.</li>
  <li><strong>GitHub Auto-Push:</strong> Automatically commits and pushes updates to a repository.</li>
  <li><strong>Clipboard Integration:</strong> Copies the latest trends to the Termux clipboard.</li>
  <li><strong>Robust Logging:</strong> Provides detailed runtime information and error handling.</li>
  <li><strong>Respectful Scraping:</strong> Includes randomized delays and request timeouts.</li>
</ul>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Project Structure</h2>

<pre>
.
├── gt_trends24_upgraded.py   # Main script
├── trends.txt                # Generated list of top hashtags
└── README.md                 # Project documentation
</pre>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Requirements</h2>

<h3>Python Dependencies</h3>

<pre><code>pip install requests beautifulsoup4
</code></pre>

<h3>System Dependencies</h3>

<ul>
  <li>Python 3.7 or later</li>
  <li>Git</li>
  <li>Termux API (optional, for clipboard functionality)</li>
</ul>

<h3>Termux Setup (Android)</h3>

<pre><code>pkg update && pkg upgrade
pkg install python git termux-api
pip install requests beautifulsoup4
termux-setup-storage
</code></pre>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Configuration</h2>

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
      <td>Directory for saving output and Git repository</td>
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

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Supported Regions</h2>

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Region</th>
      <th>URL</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>Global</td><td>https://trends24.in/</td></tr>
    <tr><td>2</td><td>USA</td><td>https://trends24.in/united-states/</td></tr>
    <tr><td>3</td><td>UK</td><td>https://trends24.in/united-kingdom/</td></tr>
    <tr><td>4</td><td>India</td><td>https://trends24.in/india/</td></tr>
    <tr><td>5</td><td>Germany</td><td>https://trends24.in/germany/</td></tr>
    <tr><td>6</td><td>Japan</td><td>https://trends24.in/japan/</td></tr>
  </tbody>
</table>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Supported Categories</h2>

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Category</th>
      <th>Example Keywords</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>General</td><td>N/A</td></tr>
    <tr><td>2</td><td>Sports</td><td>fc, vs, cup, match, league</td></tr>
    <tr><td>3</td><td>Entertainment</td><td>movie, tv, series, album, song</td></tr>
    <tr><td>4</td><td>Politics</td><td>vote, election, president, senate</td></tr>
    <tr><td>5</td><td>Technology</td><td>tech, ai, app, software, hardware, gadget, robot</td></tr>
  </tbody>
</table>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Usage</h2>

<h3>1. Clone the Repository</h3>

<pre><code>git clone https://github.com/your-username/trends24-scraper.git ~/scripts
cd ~/scripts
</code></pre>

<h3>2. Install Dependencies</h3>

<pre><code>pip install requests beautifulsoup4
</code></pre>

<h3>3. Run the Script</h3>

<pre><code>python3 gt_trends24_upgraded.py
</code></pre>

<p>
During execution, you will be prompted to select a category and one or more regions. The script will then run continuously, updating the trends at the configured interval.
</p>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Example Output</h2>

<pre>
#AI
#WorldCup
#BreakingNews
#TechTrends
#MovieNight
#Election2026
</pre>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">GitHub Auto-Push Configuration</h2>

<p>
To enable automatic commits and pushes, users must configure Git and GitHub authentication. GitHub no longer supports password-based authentication, so either a <strong>Personal Access Token (PAT)</strong> or an <strong>SSH key</strong> must be used.
</p>

<h3>1. Configure Git Identity</h3>

<pre><code>git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
</code></pre>

<h3>2. Clone the Repository to the Script Directory</h3>

<p>
Ensure that the repository is cloned into the directory specified by <code>BASE_DIR</code> (default: <code>~/scripts</code>).
</p>

<pre><code>git clone https://github.com/your-username/trends24-scraper.git ~/scripts
cd ~/scripts
</code></pre>

<h3>3. Option A: Using a Personal Access Token (HTTPS)</h3>

<ol>
  <li>Generate a token from <strong>GitHub → Settings → Developer settings → Personal access tokens</strong> with the <code>repo</code> scope.</li>
  <li>Update the remote repository URL:</li>
</ol>

<pre><code>git remote set-url origin https://&lt;USERNAME&gt;:&lt;TOKEN&gt;@github.com/&lt;USERNAME&gt;/trends24-scraper.git
</code></pre>

<p>
Replace <code>&lt;USERNAME&gt;</code> and <code>&lt;TOKEN&gt;</code> with your GitHub credentials.
</p>

<h3>4. Option B: Using SSH (Recommended)</h3>

<pre><code>ssh-keygen -t ed25519 -C "your-email@example.com"
cat ~/.ssh/id_ed25519.pub
</code></pre>

<p>
Add the generated public key to <strong>GitHub → Settings → SSH and GPG keys</strong>, then update the remote:
</p>

<pre><code>git remote set-url origin git@github.com:&lt;USERNAME&gt;/trends24-scraper.git
ssh -T git@github.com
</code></pre>

<h3>5. Verify Auto-Push</h3>

<pre><code>git add trends.txt
git commit -m "Test commit"
git push
</code></pre>

<p>
If the push succeeds without prompting for credentials, the script's auto-push functionality is correctly configured.
</p>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Automation with Cron (Optional)</h2>

<p>
Although the script runs continuously, it can be scheduled using cron if the internal loop is removed.
</p>

<pre><code>crontab -e
*/30 * * * * /usr/bin/python3 /path/to/gt_trends24_upgraded.py
</code></pre>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Logging</h2>

<p>
The script uses Python's <code>logging</code> module to provide detailed runtime information, including scraping status, file updates, and Git operations.
</p>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Disclaimer</h2>

<p>
This project is intended for educational and research purposes. Users should ensure compliance with the terms of service of Trends24. The script incorporates respectful scraping practices to minimize server load.
</p>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Contributing</h2>

<p>
Contributions are welcome. Please open an issue or submit a pull request for improvements or feature requests.
</p>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">License</h2>

<p>
This project is licensed under the MIT License. See the <code>LICENSE</code> file for details.
</p>

<h2 style="border-bottom:2px solid #eaecef; padding-bottom:6px;">Author</h2>

<p>
<strong>Kel</strong><br>
Software developer focused on automation and AI-driven solutions.
</p>
