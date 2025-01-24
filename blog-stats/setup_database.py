import sqlite3


def setup_database():
    conn = sqlite3.connect("blog_stats.db")
    cursor = conn.cursor()

    # Create articles table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS articles (
        article_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        type_of TEXT,
        tags TEXT,
        url TEXT,
        published_timestamp TEXT,
        reading_time_minutes INTEGER
    );
    """
    )

    # Create article_stats table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS article_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER NOT NULL,
        recorded_at TEXT DEFAULT (datetime('now')),
        public_reactions_count INTEGER,
        comments_count INTEGER,
        page_views_count INTEGER,
        FOREIGN KEY (article_id) REFERENCES articles(article_id)
    );
    """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    setup_database()
    print("Database setup completed.")
