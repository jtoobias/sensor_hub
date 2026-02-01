from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Sensor Dashboard"),
        html.P("If you see this, Dash works 🎉"),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
