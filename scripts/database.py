"""
Task 3: Store bank reviews in PostgreSQL database.
Uses psycopg2 for database connection and data insertion.
"""

import psycopg2
import pandas as pd


DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'bank_reviews',
    'user': 'postgres',
    'password': 'postgres123'
}


def create_connection():
    """Create connection to PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Connected to PostgreSQL database: bank_reviews")
        return conn
    except Exception as e:
        print(f"ERROR connecting: {e}")
        return None


def create_tables(conn):
    """Create banks and reviews tables."""
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS banks (
            bank_id SERIAL PRIMARY KEY,
            bank_name VARCHAR(100) NOT NULL UNIQUE,
            country VARCHAR(100) DEFAULT 'Ethiopia',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            review_id VARCHAR(255) PRIMARY KEY,
            bank_id INTEGER NOT NULL,
            review_text TEXT NOT NULL,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            sentiment_score FLOAT,
            sentiment_label VARCHAR(20),
            themes TEXT,
            review_date DATE,
            year INTEGER,
            month INTEGER,
            review_length INTEGER,
            source VARCHAR(50) DEFAULT 'Google Play',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (bank_id) REFERENCES banks(bank_id)
        )
    ''')

    conn.commit()
    print("Tables created successfully")


def insert_banks(conn):
    """Insert the three Ethiopian banks."""
    cursor = conn.cursor()
    banks = [
        ('CBE', 'Ethiopia'),
        ('BOA', 'Ethiopia'),
        ('Dashen', 'Ethiopia')
    ]
    cursor.executemany(
        'INSERT INTO banks (bank_name, country) VALUES (%s, %s) ON CONFLICT (bank_name) DO NOTHING',
        banks
    )
    conn.commit()
    print("Banks inserted successfully")


def insert_reviews(conn, df):
    """Insert all reviews using psycopg2."""
    cursor = conn.cursor()

    bank_ids = {}
    for bank_name in df['bank'].unique():
        cursor.execute('SELECT bank_id FROM banks WHERE bank_name = %s', (bank_name,))
        result = cursor.fetchone()
        if result:
            bank_ids[bank_name] = result[0]

    inserted = 0
    errors = 0

    for _, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT INTO reviews
                (review_id, bank_id, review_text, rating,
                 sentiment_score, sentiment_label, themes,
                 review_date, year, month, review_length, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (review_id) DO NOTHING
            ''', (
                str(row['review_id']),
                bank_ids.get(row['bank']),
                str(row['review']),
                int(row['rating']),
                float(row['sentiment_score']),
                str(row['sentiment_label']),
                str(row['themes']),
                str(row['date']),
                int(row['year']),
                int(row['month']),
                int(row['review_length']),
                'Google Play'
            ))
            inserted += 1
        except Exception as e:
            errors += 1
            conn.rollback()

    conn.commit()
    print(f"Reviews inserted: {inserted}, Errors: {errors}")


def verify_database(conn):
    """Run SQL queries to verify data integrity."""
    cursor = conn.cursor()

    print("\n=== DATABASE VERIFICATION ===")

    cursor.execute('''
        SELECT b.bank_name,
               COUNT(r.review_id) as total_reviews,
               ROUND(AVG(r.rating)::numeric, 2) as avg_rating,
               ROUND(AVG(r.sentiment_score)::numeric, 3) as avg_sentiment
        FROM banks b
        LEFT JOIN reviews r ON b.bank_id = r.bank_id
        GROUP BY b.bank_name
        ORDER BY avg_sentiment DESC
    ''')

    print(f"\n{'Bank':<10} {'Reviews':<10} {'Avg Rating':<12} {'Avg Sentiment'}")
    print("-" * 48)
    for row in cursor.fetchall():
        print(f"{row[0]:<10} {row[1]:<10} {row[2]:<12} {row[3]}")

    cursor.execute('''
        SELECT sentiment_label, COUNT(*) as count,
               ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM reviews), 1) as pct
        FROM reviews
        GROUP BY sentiment_label
        ORDER BY count DESC
    ''')
    print("\nSentiment breakdown:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} ({row[2]}%)")

    cursor.execute('SELECT COUNT(*) FROM banks')
    print(f"\nTotal banks: {cursor.fetchone()[0]}")
    cursor.execute('SELECT COUNT(*) FROM reviews')
    print(f"Total reviews: {cursor.fetchone()[0]}")


def main():
    try:
        df = pd.read_csv("data/raw/theme_reviews.csv")
        print(f"Loaded {len(df)} reviews")
    except Exception as e:
        print(f"ERROR loading data: {e}")
        return

    conn = create_connection()
    if not conn:
        return

    try:
        create_tables(conn)
        insert_banks(conn)
        insert_reviews(conn, df)
        verify_database(conn)
        print("\nDatabase pipeline complete!")
    except Exception as e:
        print(f"ERROR: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    main()