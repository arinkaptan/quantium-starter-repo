import dash
from dash import dcc, html, Input, Output
import pandas as pd

df = pd.read_csv("output.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

df_grouped = df.groupby("date")["sales"].sum().reset_index()

app = dash.Dash(__name__)
server = app.server 

app.layout = html.Div(style={
    "fontFamily": "Arial, sans-serif",
    "backgroundColor": "#f9f0f5",
    "padding": "30px"
}, children=[

    html.H1("Pink Morsel Sales Visualiser", style={
        "textAlign": "center",
        "color": "#c2185b",
        "fontSize": "2.5em",
        "marginBottom": "10px"
    }),

    html.P("Analyse Pink Morsel sales before and after the price increase on 15 Jan 2021.", style={
        "textAlign": "center",
        "color": "#888",
        "marginBottom": "30px"
    }),

    html.Div([
        html.Label("Filter by Region:", style={
            "fontWeight": "bold",
            "color": "#c2185b",
            "marginBottom": "10px",
            "display": "block"
        }),
        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "All", "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "South", "value": "south"},
                {"label": "East", "value": "east"},
                {"label": "West", "value": "west"},
            ],
            value="all",
            inline=True,
            style={"gap": "20px"},
            inputStyle={"marginRight": "6px"},
            labelStyle={"marginRight": "20px", "color": "#333"}
        )
    ], style={
        "backgroundColor": "white",
        "padding": "20px",
        "borderRadius": "12px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
        "marginBottom": "20px"
    }),

    dcc.Graph(id="sales-chart"),

])

@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(region):
    if region == "all":
        filtered = df.groupby("date")["sales"].sum().reset_index()
    else:
        filtered = df[df["region"] == region].groupby("date")["sales"].sum().reset_index()

    return {
        "data": [{
            "x": filtered["date"],
            "y": filtered["sales"],
            "type": "line",
            "line": {"color": "#e91e8c", "width": 2}
        }],
        "layout": {
            "xaxis": {"title": "Date"},
            "yaxis": {"title": "Sales ($)"},
            "plot_bgcolor": "white",
            "paper_bgcolor": "white",
            "shapes": [{
                "type": "line",
                "x0": "2021-01-15", "x1": "2021-01-15",
                "y0": 0, "y1": 1, "yref": "paper",
                "line": {"color": "red", "dash": "dash", "width": 2}
            }],
            "annotations": [{
                "x": "2021-01-15", "y": 1, "yref": "paper",
                "text": "Price Increase", "showarrow": True,
                "font": {"color": "red"}
            }]
        }
    }

if __name__ == "__main__":
    app.run(debug=True)