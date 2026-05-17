"""
Utility functions for the fintech review analytics pipeline.
"""


def get_bank_names():
    """Return list of banks being analyzed."""
    return ['CBE', 'BOA', 'Dashen']


def get_sentiment_label(score):
    """Convert VADER compound score to label."""
    if score >= 0.05:
        return 'positive'
    elif score <= -0.05:
        return 'negative'
    else:
        return 'neutral'


def get_app_ids():
    """Return dictionary of bank names to Google Play app IDs."""
    return {
        'CBE': 'com.combanketh.mobilebanking',
        'BOA': 'com.boa.boaMobileBanking',
        'Dashen': 'com.cr2.amolelight'
    }