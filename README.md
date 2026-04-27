# Europe Energy Interconnection — ETL Pipeline

ETL pipeline built in Python to analyze hourly energy flow data across European countries, using the [Ember Europe Electricity Interconnection Dataset](https://ember-energy.org/data/europe-electricity-interconnection-data/).

## What it does

- Extracts hourly country-level data from CSV
- Transforms and cleans the dataset (column renaming, type casting, derived fields)
- Loads results into a SQLite database with two tables:
  - `country_hourly_2024` — all 25 countries
  - `portugal_hourly_2024` — Portugal only

## Key finding

Portugal is a net electricity importer across all 24 hours of the day in 2024 — even during peak solar hours (noon–3pm), when renewable penetration exceeds 63%. High RES generation does not guarantee energy independence.

## Data

Download the dataset from [Ember's website](https://ember-energy.org/data/europe-electricity-interconnection-data/) and place the files in `data/raw/`.

## How to run

```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas
python3 etl.py
```

## Stack

- Python 3.12
- pandas
- SQLite