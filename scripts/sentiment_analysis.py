"""
Sentiment analysis script for bank app reviews.
Uses VADER to assign sentiment scores to each review.
"""

import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

# Download VADER data
nltk.download('vader_lexicon', quiet=True)


def load_clean_reviews(filepath):
    """Load preprocessed reviews."""
    try:
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} clean reviews")
        return df
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        return pd.DataFrame()
    except Exception as e:
        print(f"ERROR: {e}")
        return pd.DataFrame()


def analyze_sentiment(text):
    """
    Analyze sentiment of a single review using VADER.
    
    Returns:
        compound score between -1 (negative) and +1 (positive)
    """
    sia = SentimentIntensityAnalyzer()
    try:
        scores = sia.polarity_scores(str(text))
        return scores['compound']
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return 0.0


def classify_sentiment(score):
    """
    Classify compound score into label.
    
    Rules:
        score >= 0.05  = positive
        score <= -0.05 = negative
        between        = neutral
    """
    if score >= 0.05:
        return 'positive'
    elif score <= -0.05:
        return 'negative'
    else:
        return 'neutral'


def run_sentiment_analysis(df):
    """Apply sentiment analysis to all reviews."""
    print("\nRunning sentiment analysis...")

    # Apply VADER to each review
    df['sentiment_score'] = df['review'].apply(analyze_sentiment)

    # Classify into labels
    df['sentiment_label'] = df['sentiment_score'].apply(classify_sentiment)

    print("Sentiment analysis complete!")
    print(f"\nSentiment distribution:")
    print(df['sentiment_label'].value_counts())

    print(f"\nSentiment by bank:")
    print(df.groupby(['bank', 'sentiment_label']).size().unstack(fill_value=0))

    print(f"\nAverage sentiment score by bank:")
    print(df.groupby('bank')['sentiment_score'].mean().round(3))

    return df


def save_results(df, output_path):
    """Save sentiment results to CSV."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"\nSaved results to {output_path}")
    except Exception as e:
        print(f"ERROR saving: {e}")


def main():
    input_path = "data/raw/clean_reviews.csv"
    output_path = "data/raw/sentiment_reviews.csv"

    df = load_clean_reviews(input_path)

    if df.empty:
        print("No data to analyze")
        return

    df = run_sentiment_analysis(df)
    save_results(df, output_path)


if __name__ == '__main__':
    main()