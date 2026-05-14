"""
Preprocessing script for bank app reviews.
Cleans and prepares raw review data for sentiment analysis.
"""

import pandas as pd
import re
import os


def load_reviews(filepath):
    """Load raw reviews from CSV file."""
    try:
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} reviews from {filepath}")
        return df
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        return pd.DataFrame()
    except Exception as e:
        print(f"ERROR loading file: {e}")
        return pd.DataFrame()


def clean_text(text):
    """Clean review text by removing special characters."""
    if not isinstance(text, str):
        return ""
    # Remove extra whitespace
    text = text.strip()
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\-]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    return text


def preprocess_reviews(df):
    """
    Clean and preprocess the reviews dataframe.
    
    Steps:
    1. Remove duplicates
    2. Handle missing values
    3. Clean text
    4. Normalize dates
    5. Add derived columns
    """
    print(f"\nStarting preprocessing...")
    print(f"Initial shape: {df.shape}")

    # Remove duplicates
    df = df.drop_duplicates(subset=['review_id'])
    print(f"After removing duplicates: {df.shape}")

    # Remove missing reviews
    df = df.dropna(subset=['review', 'rating'])
    print(f"After removing missing values: {df.shape}")

    # Clean review text
    df['review'] = df['review'].apply(clean_text)

    # Remove empty reviews after cleaning
    df = df[df['review'].str.len() > 10]
    print(f"After removing short reviews: {df.shape}")

    # Normalize dates
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    # Add review length
    df['review_length'] = df['review'].apply(len)

    # Normalize rating to label
    df['rating_label'] = df['rating'].apply(
        lambda x: 'positive' if x >= 4 else ('negative' if x <= 2 else 'neutral')
    )

    print(f"\nFinal shape: {df.shape}")
    print(f"\nReviews per bank:")
    print(df['bank'].value_counts())
    print(f"\nRating distribution:")
    print(df['rating_label'].value_counts())

    return df


def save_clean_data(df, output_path):
    """Save cleaned data to CSV."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"\nSaved clean data to {output_path}")
    except Exception as e:
        print(f"ERROR saving data: {e}")


def main():
    input_path = "data/raw/bank_reviews.csv"
    output_path = "data/raw/clean_reviews.csv"

    df = load_reviews(input_path)

    if df.empty:
        print("No data to process")
        return

    df_clean = preprocess_reviews(df)
    save_clean_data(df_clean, output_path)


if __name__ == '__main__':
    main()