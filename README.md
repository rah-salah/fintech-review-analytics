# Fintech Review Analytics
## 10 Academy KAIM 9 - Week 2

Analyzing customer reviews from Ethiopian bank mobile apps to provide data-driven recommendations for product improvement.

## Banks Analyzed
- **CBE** - Commercial Bank of Ethiopia
- **BOA** - Bank of Abyssinia
- **Dashen Bank**

## Project Structure

```
fintech-review-analytics/
├── .github/workflows/unittests.yml
├── data/raw/
├── notebooks/task1_eda.ipynb
├── scripts/
│   ├── scrape_reviews.py
│   ├── preprocess_reviews.py
│   ├── sentiment_analysis.py
│   └── theme_extraction.py
├── src/__init__.py
├── tests/test_preprocess.py
├── .gitignore
├── requirements.txt
└── README.md
```

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
```

### 4. Run tests
```bash
pytest tests/ -v
```

## Key Findings
- **1,200 reviews** collected (400 per bank)
- **683 clean reviews** after preprocessing
- **Dashen** has highest user satisfaction (avg sentiment: 0.242)
- **BOA** has most negative reviews (lowest sentiment: 0.087)
- **App Performance** is the most complained about theme

## Data Sources
- Google Play Store reviews via google-play-scraper
- Language: English, Country: Ethiopia

## Tasks
- **Task 1** - Data collection and preprocessing
- **Task 2** - Sentiment analysis and theme extraction
- **Task 3** - Database storage (PostgreSQL/SQLite)
- **Task 4** - Visualizations and recommendations