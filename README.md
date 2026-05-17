# Fintech Review Analytics
## 10 Academy KAIM 9 - Week 2 | Omega Consultancy

Analyzing customer reviews from three Ethiopian bank mobile apps to provide
data-driven recommendations for product improvement.

## Banks Analyzed
- **CBE** - Commercial Bank of Ethiopia (com.combanketh.mobilebanking)
- **BOA** - Bank of Abyssinia (com.boa.boaMobileBanking)
- **Dashen Bank** (com.cr2.amolelight)

## Key Findings
- **1,200 reviews** collected (400 per bank)
- **683 clean reviews** after preprocessing
- **Dashen** has highest satisfaction (avg sentiment: 0.242)
- **BOA** has most complaints (avg sentiment: 0.087, 26% negative)
- **App Performance** is the top complaint theme (101 mentions)

## Project Structure

```
fintech-review-analytics/
├── .github/workflows/unittests.yml
├── data/
│   ├── raw/
│   └── chart*.png
├── notebooks/
│   ├── task1_eda.ipynb
│   └── task4_visualization.ipynb
├── scripts/
│   ├── scrape_reviews.py
│   ├── preprocess_reviews.py
│   ├── sentiment_analysis.py
│   ├── theme_extraction.py
│   └── database.py
├── src/
│   └── utils.py
├── tests/
│   └── test_preprocess.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Scraping Methodology
- Tool: google-play-scraper Python library
- Reviews per bank: 400 most recent English reviews
- Sort: Newest first
- Date range: 2023 to May 2026
- Fields collected: review text, rating, date, bank name, source

## Scraping Limitations
- English language reviews only
- Maximum 400 reviews per bank
- 683 of 1200 reviews retained after preprocessing (57%)
- Dashen initial app ID was incorrect, resolved by testing alternatives

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/rah-salah/fintech-review-analytics.git
cd fintech-review-analytics
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the full pipeline
```bash
python scripts/scrape_reviews.py
python scripts/preprocess_reviews.py
python scripts/sentiment_analysis.py
python scripts/theme_extraction.py
python scripts/database.py
```

### 4. Run tests
```bash
pytest tests/ -v
```

## Tasks Completed
- **Task 1** - Data collection (1,200 reviews) and preprocessing (683 clean)
- **Task 2** - VADER sentiment analysis and keyword theme extraction
- **Task 3** - PostgreSQL database with banks and reviews tables via psycopg2
- **Task 4** - 5 visualizations and bank-specific recommendations

## Data Sources
- Google Play Store via google-play-scraper
- Language: English, Country: Ethiopia
