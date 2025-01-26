from flask import Flask, jsonify
from queries import get_data
from flask_caching import Cache

app = Flask(__name__)
timeout = 86400  # Cache expires in 1 day (24 hours)

# Configure cache
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = timeout
cache = Cache(app)


@app.route("/stats", methods=["GET"])
@cache.cached(timeout=timeout)
def get_stats():
    data = get_data()
    total_reactions = 0
    total_comments = 0
    total_views = 0
    titles = []

    for key in data:
        article = data[key]
        total_reactions += article.get("public_reactions_count", [0])[-1]
        total_comments += article.get("comments_count", [0])[-1]
        total_views += article.get("page_views_count", [0])[-1]
        titles.append(article["title"])
    return jsonify(
        {
            "data": data,
            "total_reactions": total_reactions,
            "total_comments": total_comments,
            "total_views": total_views,
            "titles": titles,
        }
    )


if __name__ == "__main__":
    app.run(port=5001)
