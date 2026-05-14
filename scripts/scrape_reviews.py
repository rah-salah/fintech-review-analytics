from google_play_scraper import reviews, Sort
import pandas as pd
import os

# App IDs for each bank on Google Play Store
APPS = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen': 'com.cr2.amolelight'
}

def scrape_bank_reviews(bank_name, app_id, count=400):
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
        print(f"Got {len(df)} reviews for {bank_name}")
        return df
    except Exception as e:
        print(f"Error scraping {bank_name}: {e}")
        return pd.DataFrame()

def main():
    all_reviews = []
    
    for bank_name, app_id in APPS.items():
        df = scrape_bank_reviews(bank_name, app_id, count=400)
        if not df.empty:
            all_reviews.append(df)
    
    if all_reviews:
        combined = pd.concat(all_reviews, ignore_index=True)
        
        # Keep only needed columns
        combined = combined[['reviewId', 'content', 'score', 
                             'at', 'bank', 'source']]
        
        # Rename columns
        combined.columns = ['review_id', 'review', 'rating', 
                           'date', 'bank', 'source']
        
        # Clean dates
        combined['date'] = pd.to_datetime(combined['date']).dt.date
        
        # Remove duplicates
        combined = combined.drop_duplicates(subset='review_id')
        
        # Remove missing reviews
        combined = combined.dropna(subset=['review', 'rating'])
        
        print(f"\nTotal reviews collected: {len(combined)}")
        print(combined['bank'].value_counts())
        
        # Save to CSV
        os.makedirs('data/raw', exist_ok=True)
        combined.to_csv('data/raw/bank_reviews.csv', index=False)
        print("\nSaved to data/raw/bank_reviews.csv")
    else:
        print("No reviews collected")

if __name__ == '__main__':
    main()