"""
Task 1: Scrape reviews from Google Play Store for Ethiopian banks.
Collects 400+ reviews per bank and saves to CSV.
"""

from google_play_scraper import reviews, Sort
import pandas as pd
import os


APPS = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen': 'com.cr2.amolelight'
}


def scrape_bank_reviews(bank_name, app_id, count=400):
    """Scrape reviews for a single bank app."""
    print(f"Scraping {bank_name}...")
    try:
        result, _ = reviews(
            app_id,
            lang='en',
            country='et',
            sort=Sort.NEWEST,
            count=count
        )
        df = pd.DataFrame(result)
        df['bank'] = bank_name
        df['source'] = 'Google Play'
        print(f"  Collected {len(df)} reviews for {bank_name}")
        return df
    except Exception as e:
        print(f"  ERROR scraping {bank_name}: {e}")
        return pd.DataFrame()


def combine_and_clean(all_dfs):
    """Combine all bank reviews and select needed columns."""
    combined = pd.concat(all_dfs, ignore_index=True)
    combined = combined[['reviewId', 'content', 'score', 'at', 'bank', 'source']]
    combined.columns = ['review_id', 'review', 'rating', 'date', 'bank', 'source']
    combined['date'] = pd.to_datetime(combined['date']).dt.date
    combined = combined.drop_duplicates(subset='review_id')
    combined = combined.dropna(subset=['review', 'rating'])
    return combined


def main():
    all_reviews = []

    for bank_name, app_id in APPS.items():
        df = scrape_bank_reviews(bank_name, app_id, count=400)
        if not df.empty:
            all_reviews.append(df)

    if not all_reviews:
        print("ERROR: No reviews collected")
        return

    combined = combine_and_clean(all_reviews)

    print(f"\nTotal reviews collected: {len(combined)}")
    print(combined['bank'].value_counts())

    os.makedirs('data/raw', exist_ok=True)
    combined.to_csv('data/raw/bank_reviews.csv', index=False)
    print("Saved to data/raw/bank_reviews.csv")


if __name__ == '__main__':
    main()