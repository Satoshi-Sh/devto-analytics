from flask import Flask, jsonify
from queries import get_data

app = Flask(__name__)


@app.route("/stats", methods=["GET"])
def get_stats():
    data = get_data()
    return jsonify(data)


if __name__ == "__main__":
    app.run(port=5001)
