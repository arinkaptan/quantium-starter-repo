import dash
from dash import dcc, html
import pandas as pd

df = pd.read_csv("output.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

df_grouped = df.groupby("date")["sales"].sum().reset_index()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser"),
    
    dcc.Graph(
        id="sales-chart",
        figure={
            "data": [
                {
                    "x": df_grouped["date"],
                    "y": df_grouped["sales"],
                    "type": "line",
                    "name": "Sales"
                }
            ],
            "layout": {
                "title": "Pink Morsel Sales Over Time",
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "Sales ($)"},
                "shapes": [{
                    "type": "line",
                    "x0": "2021-01-15",
                    "x1": "2021-01-15",
                    "y0": 0,
                    "y1": 1,
                    "yref": "paper",
                    "line": {"color": "red", "dash": "dash"}
                }],
                "annotations": [{
                    "x": "2021-01-15",
                    "y": 1,
                    "yref": "paper",
                    "text": "Price Increase",
                    "showarrow": True
                }]
            }
        }
    )
])

if __name__ == "__main__":
    app.run(debug=True)