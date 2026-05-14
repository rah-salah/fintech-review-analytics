"""
Unit tests for preprocessing functions.
"""

import pytest
import pandas as pd
import sys
sys.path.append('scripts')

from preprocess_reviews import clean_text, preprocess_reviews


def test_clean_text_removes_special_chars():
    """Test that special characters are removed."""
    result = clean_text("Hello @World! #test")
    assert '@' not in result
    assert '#' not in result


def test_clean_text_handles_empty():
    """Test that empty string is handled."""
    result = clean_text("")
    assert result == ""


def test_clean_text_handles_none():
    """Test that None is handled."""
    result = clean_text(None)
    assert result == ""


def test_preprocess_removes_duplicates():
    """Test that duplicates are removed."""
    df = pd.DataFrame({
        'review_id': ['1', '1', '2'],
        'review': ['good app', 'good app', 'bad app'],
        'rating': [5, 5, 1],
        'date': ['2023-01-01', '2023-01-01', '2023-01-02'],
        'bank': ['CBE', 'CBE', 'BOA'],
        'source': ['Google Play', 'Google Play', 'Google Play']
    })
    result = preprocess_reviews(df)
    assert len(result) < 3


def test_preprocess_adds_rating_label():
    """Test that rating labels are added correctly."""
    df = pd.DataFrame({
        'review_id': ['1', '2', '3'],
        'review': ['great app very good', 'terrible app crashes', 'okay app works'],
        'rating': [5, 1, 3],
        'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'bank': ['CBE', 'BOA', 'Dashen'],
        'source': ['Google Play', 'Google Play', 'Google Play']
    })
    result = preprocess_reviews(df)
    assert 'rating_label' in result.columns
    assert 'positive' in result['rating_label'].values
    assert 'negative' in result['rating_label'].values


if __name__ == '__main__':
    pytest.main([__file__, '-v'])