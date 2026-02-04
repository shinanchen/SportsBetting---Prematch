# OpticOdds NFL Pre-Match Moneyline Dataset Builder

This repository contains a Python-based data pipeline for collecting, structuring, and analyzing **NFL pre-event (prematch) moneyline odds** across multiple sportsbooks using the **OpticOdds API**.

The project focuses on **cross-sportsbook price comparison for the same NFL match**, ensuring that both teams’ moneylines are captured **before kickoff**.

---

## 📌 Project Scope

### What this project does
- Retrieves NFL fixtures for selected seasons (2022–2025)
- Filters to **Regular Season and Playoffs only**
- Identifies fixtures eligible for moneyline markets
- Collects **prematch moneyline odds** across multiple sportsbooks
- Stores both teams’ moneylines for the same match
- Produces clean, analysis-ready datasets (CSV / Parquet)

### What this project does NOT do
- Reconstruct historical prematch odds after games have completed
- Use OpticOdds AI or premium historical odds products
- Collect in-play or live odds

> ⚠️ OpticOdds snapshot endpoints only guarantee odds for upcoming or live fixtures.  
> Full historical prematch reconstruction requires premium access.

---

## 📁 Repository Structure
opticodds/
│
├── opticodds_client.py # Lightweight OpticOdds REST client
├── stream_odds.py # Live odds streaming (SSE)
├── collect_fixtures.py # NFL fixture discovery by season
├── collect_moneyline.py # Prematch moneyline collection
│
├── odds.ipynb # Exploration and debugging notebook
├── requirements.txt
├── README.md
│
└── data/
├── fixtures/
├── moneyline_snapshots/
└── final_datasets/

📎 Disclaimer

This project is for research and educational purposes only.
It does not constitute betting or financial advice.
