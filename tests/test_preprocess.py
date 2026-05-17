"""
Unit tests for preprocessing and sentiment functions.
"""

import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from preprocess_reviews import clean_text, add_rating_label, preprocess_reviews
from sentiment_analysis import analyze_sentiment, classify_sentiment


# --- clean_text tests ---

def test_clean_text_removes_special_chars():
    result = clean_text("Hello @World! #test")
    assert '@' not in result
    assert '#' not in result

def test_clean_text_handles_empty():
    result = clean_text("")
    assert result == ""

def test_clean_text_handles_none():
    result = clean_text(None)
    assert result == ""

def test_clean_text_strips_whitespace():
    result = clean_text("  hello world  ")
    assert result == "hello world"


# --- add_rating_label tests ---

def test_rating_label_positive():
    assert add_rating_label(5) == 'positive'
    assert add_rating_label(4) == 'positive'

def test_rating_label_negative():
    assert add_rating_label(1) == 'negative'
    assert add_rating_label(2) == 'negative'

def test_rating_label_neutral():
    assert add_rating_label(3) == 'neutral'


# --- classify_sentiment tests ---

def test_classify_positive():
    assert classify_sentiment(0.5) == 'positive'
    assert classify_sentiment(0.05) == 'positive'

def test_classify_negative():
    assert classify_sentiment(-0.5) == 'negative'
    assert classify_sentiment(-0.05) == 'negative'

def test_classify_neutral():
    assert classify_sentiment(0.0) == 'neutral'
    assert classify_sentiment(0.04) == 'neutral'


# --- preprocess_reviews tests ---

def make_sample_df():
    return pd.DataFrame({
        'review_id': ['1', '1', '2', '3'],
        'review': ['great app very good', 'great app very good',
                   'terrible crashes always', 'ok'],
        'rating': [5, 5, 1, 3],
        'date': ['2023-01-01', '2023-01-01',
                 '2023-01-02', '2023-01-03'],
        'bank': ['CBE', 'CBE', 'BOA', 'Dashen'],
        'source': ['Google Play'] * 4
    })

def test_preprocess_removes_duplicates():
    df = make_sample_df()
    result = preprocess_reviews(df)
    assert result['review_id'].duplicated().sum() == 0

def test_preprocess_adds_rating_label():
    df = make_sample_df()
    result = preprocess_reviews(df)
    assert 'rating_label' in result.columns

def test_preprocess_adds_year_month():
    df = make_sample_df()
    result = preprocess_reviews(df)
    assert 'year' in result.columns
    assert 'month' in result.columns

def test_preprocess_adds_review_length():
    df = make_sample_df()
    result = preprocess_reviews(df)
    assert 'review_length' in result.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
