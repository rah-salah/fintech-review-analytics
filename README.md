# Fintech Review Analytics - Week 2

## Project Overview

This project analyzes customer reviews from three major Ethiopian bank
mobile apps on Google Play Store on behalf of Omega Consultancy.

We scrape, clean, and analyze over 1,200 reviews to identify sentiment
patterns and recurring themes that help banks prioritize improvements.

## Target Banks

| Bank   | Full Name                   | App ID                       |
| ------ | --------------------------- | ---------------------------- |
| CBE    | Commercial Bank of Ethiopia | com.combanketh.mobilebanking |
| BOA    | Bank of Abyssinia           | com.boa.boaMobileBanking     |
| Dashen | Dashen Bank                 | com.cr2.amolelight           |

## Scraping Methodology

- Tool: google-play-scraper Python library
- Reviews per bank: 400 (most recent English reviews)
- Sort order: Newest first
- Date range: Reviews collected up to May 2026
- Fields collected: review text, rating, date, bank name, source

## Scraping Limitations

- Only English language reviews were collected
- Maximum 400 reviews per bank due to API constraints
- Reviews older than the app's update cycle may not reflect current UX
- After preprocessing, 685 of 1,200 reviews remained usable

## Setup Instructions

### 1. Clone the repository

git clone https://github.com/rah-salah/fintech-review-analytics.git
cd fintech-review-analytics

### 2. Install dependencies

pip install -r requirements.txt

### 3. Run scraping

python scripts/scrape_reviews.py

### 4. Run preprocessing

python scripts/preprocess_reviews.py

### 5. Run sentiment analysis

python scripts/sentiment_analysis.py

## Project Structure

fintech-review-analytics/
├── .github/workflows/ # CI/CD pipeline
├── data/raw/ # Raw and processed data (not committed)
├── notebooks/ # Jupyter notebooks for EDA
├── scripts/ # Python scripts
│ ├── scrape_reviews.py
│ ├── preprocess_reviews.py
│ ├── sentiment_analysis.py
│ └── theme_extraction.py
├── src/ # Source modules
├── tests/ # Unit tests
├── requirements.txt
└── README.md

## Key Findings

- Dashen Bank: highest user satisfaction (avg sentiment: 0.242)
- BOA: most negative reviews (61 negative, avg sentiment: 0.084)
- Top complaint theme: App Performance (101 mentions)
- Top praise theme: Transaction speed and UI design
