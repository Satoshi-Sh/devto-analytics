import sqlite3


# Query to fetch all stats data with article details
QUERY = """
    SELECT 
        articles.title, 
        articles.article_id,
        articles.tags,
        articles.url,
        articles.published_timestamp, 
        article_stats.recorded_at,
        article_stats.page_views_count, 
        article_stats.comments_count, 
        article_stats.public_reactions_count
    FROM 
        articles
    INNER JOIN 
        article_stats 
    ON 
        articles.article_id = article_stats.article_id
    ORDER BY 
        article_stats.recorded_at
"""


def get_db_connection():
    conn = sqlite3.connect("../blog-stats/blog_stats.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_data():
    """Retrieve the latest stats for each article."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(QUERY)
    rows = cursor.fetchall()
    articles = {}
    for row in rows:
        (
            title,
            article_id,
            tags,
            url,
            published_timestamp,
            recorded_at,
            page_views_count,
            comments_count,
            public_reactions_count,
        ) = row

        if article_id not in articles:
            articles[article_id] = {
                "title": title,
                "tags": tags.split(","),
                "url": url,
                "published_timestamp": published_timestamp,
                "recorded_at": [recorded_at],
                "page_views_count": [page_views_count],
                "comments_count": [comments_count],
                "public_reactions_count": [public_reactions_count],
            }
        else:
            a = articles[article_id]
            a["recorded_at"].append(recorded_at)
            a["page_views_count"].append(page_views_count)
            a["comments_count"].append(comments_count)
            a["public_reactions_count"].append(public_reactions_count)
    conn.close()
    return articles
