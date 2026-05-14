"""
Theme extraction script for bank app reviews.
Identifies recurring topics and themes in reviews.
"""

import pandas as pd
from collections import Counter
import re
import os


# Define financial app themes and their keywords
THEMES = {
    'Login & Authentication': [
        'login', 'password', 'otp', 'fingerprint',
        'biometric', 'sign in', 'authentication', 'locked'
    ],
    'Transaction & Transfer': [
        'transfer', 'transaction', 'send money', 'payment',
        'withdraw', 'deposit', 'balance', 'money'
    ],
    'App Performance': [
        'crash', 'slow', 'freeze', 'bug', 'error',
        'loading', 'speed', 'fast', 'performance'
    ],
    'User Interface': [
        'design', 'interface', 'easy', 'difficult',
        'navigation', 'user friendly', 'simple', 'complicated'
    ],
    'Customer Service': [
        'support', 'service', 'help', 'response',
        'customer care', 'agent', 'staff', 'complaint'
    ],
    'Network & Connectivity': [
        'network', 'internet', 'connection', 'offline',
        'server', 'timeout', 'failed', 'unavailable'
    ]
}


def identify_themes(text):
    """
    Identify themes present in a review.
    Returns list of themes found.
    """
    text = str(text).lower()
    found_themes = []

    for theme, keywords in THEMES.items():
        for keyword in keywords:
            if keyword in text:
                found_themes.append(theme)
                break

    return found_themes if found_themes else ['General']


def extract_themes(df):
    """Apply theme extraction to all reviews."""
    print("Extracting themes from reviews...")

    df['themes'] = df['review'].apply(identify_themes)

    # Count theme frequency
    all_themes = []
    for themes in df['themes']:
        all_themes.extend(themes)

    theme_counts = Counter(all_themes)

    print("\nTheme frequency across all banks:")
    for theme, count in theme_counts.most_common():
        print(f"  {theme}: {count}")

    return df, theme_counts


def analyze_themes_by_bank(df):
    """Analyze themes per bank."""
    print("\nTheme analysis by bank:")

    for bank in df['bank'].unique():
        bank_df = df[df['bank'] == bank]
        bank_themes = []
        for themes in bank_df['themes']:
            bank_themes.extend(themes)

        bank_theme_counts = Counter(bank_themes)
        print(f"\n{bank} top themes:")
        for theme, count in bank_theme_counts.most_common(3):
            print(f"  - {theme}: {count} mentions")


def save_results(df, output_path):
    """Save theme results."""
    try:
        df['themes'] = df['themes'].apply(lambda x: ', '.join(x))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"\nSaved to {output_path}")
    except Exception as e:
        print(f"ERROR: {e}")


def main():
    input_path = "data/raw/sentiment_reviews.csv"
    output_path = "data/raw/theme_reviews.csv"

    try:
        df = pd.read_csv(input_path)
        print(f"Loaded {len(df)} reviews")
    except Exception as e:
        print(f"ERROR: {e}")
        return

    df, theme_counts = extract_themes(df)
    analyze_themes_by_bank(df)
    save_results(df, output_path)


if __name__ == '__main__':
    main()