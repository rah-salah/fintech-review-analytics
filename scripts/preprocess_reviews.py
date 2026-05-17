"""
Task 1: Preprocess and clean raw bank reviews.
Handles missing values, duplicates, and text cleaning.
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
    """Clean review text by removing noise."""
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = re.sub(r'[^\w\s\.\,\!\?\-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def add_rating_label(rating):
    """Convert numeric rating to sentiment label."""
    if rating >= 4:
        return 'positive'
    elif rating <= 2:
        return 'negative'
    else:
        return 'neutral'


def preprocess_reviews(df):
    """
    Full preprocessing pipeline.
    Steps: remove duplicates, handle missing values,
    clean text, normalize dates, add derived columns.
    """
    print(f"Starting preprocessing...")
    print(f"Initial shape: {df.shape}")

    df = df.drop_duplicates(subset=['review_id'])
    print(f"After removing duplicates: {df.shape}")

    df = df.dropna(subset=['review', 'rating'])
    print(f"After removing missing values: {df.shape}")

    df = df.copy()
    df['review'] = df['review'].apply(clean_text)
    df = df[df['review'].str.len() > 10]
    print(f"After removing short reviews: {df.shape}")

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['review_length'] = df['review'].apply(len)
    df['rating_label'] = df['rating'].apply(add_rating_label)

    print(f"Final shape: {df.shape}")
    print(f"Reviews per bank:")
    print(df['bank'].value_counts())

    return df


def save_clean_data(df, output_path):
    """Save cleaned data to CSV."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Saved clean data to {output_path}")
    except Exception as e:
        print(f"ERROR saving: {e}")


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
