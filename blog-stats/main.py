from setup_database import setup_database
from collect_data import get_data
from insert_data import insert_articles, insert_article_stats


def main():
    # Setup database (if not already set up)
    setup_database()

    # Fetch articles from API
    articles = get_data()
    if not articles:
        print("No articles fetched.")
        return

    # Insert articles and stats into the database
    insert_articles(articles)
    insert_article_stats(articles)

    print("Data successfully fetched and stored!")


if __name__ == "__main__":
    main()
