import requests
from taipy.gui import Gui, State

URL = "localhost:5001"


def get_data():
    response = requests.get("http://localhost:5001/stats")
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
    return response.json()


def initialize_stats():
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

    return data, total_reactions, total_comments, total_views, titles


def update_column(state: State, var_name: str, value: str):
    print(f"Selected column: {value}")
    state.selected_column = value


def update_title(state: State, var_name: str, value: list):
    print(f"Selected titles: {value}")
    state.selected_titles = value


data, total_reactions, total_comments, total_views, titles = initialize_stats()
columns = ["public_reactions_count", "comments_count", "page_views_count"]
selected_column = columns[0]
selected_titles = titles[:-3]

# GUI
page = """
# DevTo Stats

<|layout|columns=1 1 1|
<|card text-center|
**Total Reactions**
##<|{str(total_reactions)}|text|format=,.0f|>
|>

<|card text-center|
**Total Comments**
##<|{str(total_comments)}|text|format=,.0f|>
|>

<|card text-center|
**Total Views**
##<|{str(total_views)}|text|format=,.0f|>
|>
|>

## Plots
<|layout|columns=1 1| 
<|part|
#### Column:
<|{selected_column}|selector|lov={columns}|on_change=update_column|dropdown|>
|>
<|part|
#### Posts:
<|{selected_titles}|selector|lov={titles}|multiple|dropdown|on_change=update_title|>
|>
|>
"""

# Create a Taipy GUI
gui = Gui(page)

if __name__ == "__main__":
    gui.run(port=5002, dark_mode=False, title="DevTo Stats Dashboard")
