# SportsBetting---Prematch
OpticOdds NFL Moneyline Dataset Builder

This repository contains a Python pipeline for collecting, structuring, and analyzing NFL pre-event (prematch) moneyline odds across multiple sportsbooks using the OpticOdds API.

The project is designed to:

Discover NFL fixtures by season

Identify games that had moneyline markets

Collect sportsbook-level moneyline odds before kickoff

Build a clean, match-level dataset for cross-sportsbook comparison

📌 Project Scope
What this project does

Pulls NFL fixtures for selected seasons (2022–2025)

Filters to Regular Season & Playoffs only

Ensures fixtures are eligible for moneyline markets

Collects prematch moneyline odds across sportsbooks

Stores both teams’ moneylines for the same match

Produces analysis-ready datasets (CSV / Parquet)

What this project does not do

Reconstruct historical prematch odds after games have completed

Use OpticOdds AI / premium historical endpoints

Collect live or in-play odds

⚠️ OpticOdds snapshot endpoints only guarantee odds for upcoming or live fixtures. Historical prematch odds require special access.

📁 Repository Structure
opticodds/
│
├── opticodds_client.py      # Thin OpticOdds REST client
├── stream_odds.py           # Live odds streaming (SSE)
├── collect_fixtures.py      # Fixture discovery by season
├── collect_moneyline.py     # Prematch moneyline collection
│
├── odds.ipynb               # Exploration & debugging notebook
├── requirements.txt
├── README.md
│
└── data/
    ├── fixtures/
    ├── moneyline_snapshots/
    └── final_datasets/

🔑 Authentication

The API key is never hardcoded.

Set your key as an environment variable:

export OPTICODDS_API_KEY="your_api_key_here"


Or use a .env file (recommended for notebooks):

OPTICODDS_API_KEY=your_api_key_here

🧠 Data Model (Core Fields)

Each moneyline observation contains:

Field	Description
fixture_id	Unique OpticOdds fixture identifier
game_id	Stable game identifier
season_year	NFL season
season_week	Week number
season_type	Regular Season / Playoffs
sportsbook	Sportsbook name
team	Team name
side	home / away
price	American odds
is_live	False (prematch only)
timestamp	Odds timestamp (UTC)
kickoff_ts	Game kickoff time (UTC)
🛠 Step-by-Step Workflow
Step 1 — Discover Fixtures

Pull NFL fixtures by season and filter to:

Regular Season

Playoffs

has_odds == True

fixtures = get("/fixtures/active", params={
    "sport": "football",
    "league": "nfl",
})

Step 2 — Filter Eligible Games

Remove:

Preseason games

Fixtures without moneyline markets

Fixtures without valid kickoff timestamps

Result:

~559 NFL fixtures with moneyline eligibility (2023–2025)

Step 3 — Collect Sportsbooks

Retrieve active sportsbooks (global):

sportsbooks = get("/sportsbooks/active")["data"]


Sportsbooks are queried in batches of 1–5 to comply with API limits.

Step 4 — Collect Prematch Moneyline Odds

For each fixture:

Query snapshot odds

Filter to:

market == moneyline

is_live == False

timestamp < kickoff_ts

Store both teams’ moneylines

get("/fixtures/odds", params={
    "fixture_id": fixture_id,
    "market": "moneyline",
    "sportsbook": sportsbook_batch,
})

Step 5 — Storage

Supported formats:

CSV (default)

Parquet (optional, requires pyarrow)

conda install pyarrow

⚠️ Important API Notes

has_odds=True means odds existed at some point, not necessarily retrievable now

Snapshot endpoints do not provide full historical reconstruction

Completed games may return:

empty odds

only live odds

no prematch data

This is expected behavior.

📊 Intended Analysis Use Cases

Cross-sportsbook price dispersion

Implied probability disagreement

Favorite vs underdog pricing bias

Market efficiency tests (prematch)

Arbitrage opportunity detection (real-time use)

🧪 Environment

Python 3.11

Conda environment recommended

Key dependencies:

requests

pandas

python-dotenv

sseclient-py (streaming)

🚀 Next Extensions

Automated daily prematch collection

Closing-line vs opening-line comparison

Integration with betting strategy backtests

Multi-sport expansion (NBA, MLB, NHL)

📎 Disclaimer

This project is for research and educational purposes only.
No betting or financial advice is provided.
