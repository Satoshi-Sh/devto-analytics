import sqlite3


def insert_articles(data):
    conn = sqlite3.connect("blog_stats.db")
    cursor = conn.cursor()
    for article in data:
        cursor.execute(
            """
        INSERT OR IGNORE INTO articles (
            article_id,
            title,
            type_of,
            tags,
            url,
            published_timestamp,
            reading_time_minutes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                article["id"],
                article["title"],
                article["type_of"],
                ",".join(article["tag_list"]),
                article["url"],
                article["published_timestamp"],
                article["reading_time_minutes"],
            ),
        )

    conn.commit()
    conn.close()


def insert_article_stats(data):
    conn = sqlite3.connect("blog_stats.db")
    cursor = conn.cursor()

    for article in data:
        cursor.execute(
            """
        INSERT INTO article_stats (
            article_id,
            public_reactions_count,
            comments_count,
            page_views_count
        )
        VALUES (?, ?, ?, ?)
        """,
            (
                article["id"],
                article["public_reactions_count"],
                article["comments_count"],
                article["page_views_count"],
            ),
        )

    conn.commit()
    conn.close()
