# ETL Pipeline Project

A simple Python-based ETL pipeline for ingesting ecommerce CSV data, cleaning it, and loading it into a PostgreSQL database.

## Project Overview

This repository contains an ETL workflow that:
- reads raw CSV files from `data/`
- cleans and normalizes the data using reusable transformation functions
- writes the cleaned data into PostgreSQL tables via `src/database.py`

## Key Components

- `src/main.py` - primary ETL entry point for executing the full pipeline
- `src/all.py` - helper module for loading CSV files into pandas DataFrames
- `src/clean.py` - data cleaning utilities for users, products, sessions, interactions, purchases, and reviews
- `src/database.py` - PostgreSQL database connection and insert logic
- `src/readers/csv_reader.py` - CSV file reader utilities
- `tests/` - unit tests for extract, transform, and load functionality
- `config/` - project configuration files
- `data/` - sample CSV source data files

## Repository Structure

- `config/sources.yml` - data source metadata and configuration
- `data/` - raw CSV files used by the pipeline
- `src/` - ETL source code
- `tests/` - pytest test cases

## Requirements

The pipeline depends on:
- Python 3.8+ (or later)
- pandas
- psycopg2
- python-dotenv
- pytest

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install pandas psycopg2-binary python-dotenv pytest
```

3. Create a `.env` file in the repository root or next to `src/database.py` with your PostgreSQL credentials:

```env
DB_HOST=localhost
DATABASE=your_database
USER=your_username
PASSWORD=your_password
PORT=5432
```

## Running the Pipeline

From the repository root:

```bash
python -m src.main

To run Tkinter
python -m src.tkinter_app

```

## Running Tests

Execute the test suite with:

```bash
python -m pytest tests/test_extract.py
python -m pytest tests/test_load.py
python -m pytest tests/test_transform.py
```

This will:
- initialize database tables
- read raw CSV files from `data/`
- clean each dataset
- insert cleaned records into PostgreSQL



## Notes

- `src/main.py` is the main pipeline orchestrator.
- `src/clean.py` contains generic cleaning plus dataset-specific date conversions.
- `src/database.py` handles database schema creation and inserts.
- `data/` should contain the source CSV files required by the ETL.

## License

This project is provided as-is for educational and development purposes.

