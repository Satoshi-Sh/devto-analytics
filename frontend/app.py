import requests
from taipy.gui import Gui, State
import plotly.graph_objects as go

URL = "localhost:5001"


def get_data():
    response = requests.get("http://localhost:5001/stats")
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return {
            "data": {},
            "total_reactions": 0,
            "total_comments": 0,
            "total_views": 0,
            "titles": [],
        }
    return response.json()


def create_plot(data, articles, column):
    figure = go.Figure()
    for key in data:
        article = data[key]
        if article["title"] in articles:
            print(article)
            figure.add_trace(
                go.Scatter(
                    x=article["recorded_at"],
                    y=article[column],
                    mode="lines",
                    name=article["title"],
                )
            )
    column = column.replace("_", " ").title()
    figure.update_layout(
        title=f"{column} Daily Growth",
        xaxis_title="Date",
        yaxis_title=column,
        legend_title="Article",
        xaxis=dict(
            tickformat="%Y-%m-%d"  # Format the x-axis ticks to show only the date (YYYY-MM-DD)
        ),
    )
    return figure


def update_column(state: State, var_name: str, value: str):
    state.selected_column = value
    state.figure = create_plot(data, state.selected_titles, state.selected_column)


def update_title(state: State, var_name: str, value: list):
    state.selected_titles = value
    state.figure = create_plot(data, state.selected_titles, state.selected_column)


result = get_data()
data = result["data"]
total_reactions = result["total_reactions"]
total_comments = result["total_comments"]
total_views = result["total_views"]
titles = result["titles"]
columns = ["public_reactions_count", "comments_count", "page_views_count"]
selected_column = columns[2]
selected_titles = titles[:-3]
figure = create_plot(data, selected_titles, selected_column)

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
<|chart|figure={figure}|>
"""

# Create a Taipy GUI
gui = Gui(page)

if __name__ == "__main__":
    gui.run(port=5002, dark_mode=False, title="DevTo Stats Dashboard")
