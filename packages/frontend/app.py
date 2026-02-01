from dash import Dash, html, dcc, Input, Output, ALL, callback, exceptions
import plotly.graph_objs as go
import random
import time

# -----------------------
# Fake backend data
# -----------------------

DEVICES = {
    "node_01": {
        "name": "Greenhouse",
        "rssi": -72,
        "battery": 3.92,
        "sensors": {
            "temperature": [20 + random.random() for _ in range(20)],
            "humidity": [55 + random.random() for _ in range(20)],
        },
    },
    "node_02": {
        "name": "Garage",
        "rssi": -65,
        "battery": 4.05,
        "sensors": {
            "temperature": [15 + random.random() for _ in range(20)],
        },
    },
}

# -----------------------
# Dash app
# -----------------------
app = Dash(__name__, suppress_callback_exceptions=True)


def sidebar():
    return html.Div(
        children=[
            html.H3("Devices"),
            html.Ul(
                [
                    html.Li(
                        f"{device_id} – {device['name']}",
                        id={"type": "device", "index": device_id},
                        n_clicks=0,
                        style={"cursor": "pointer"},
                    )
                    for device_id, device in DEVICES.items()
                ]
            ),
        ],
        style={
            "width": "25%",
            "borderRight": "1px solid #ddd",
            "padding": "10px",
        },
    )

app.layout = html.Div(
    children=[
        sidebar(),
        html.Div(
            id="main",
            children=[html.H2("Select a device")],
            style={"width": "75%", "padding": "20px"},
        ),
    ],
    style={"display": "flex"},
)

# -----------------------
# Device selection
# -----------------------

@callback(
    Output("main", "children"),
    Input({"type": "device", "index": ALL}, "n_clicks"),
)
def select_device(n_clicks):
    if not any(n_clicks):
        return html.H2("Select a device")

    idx = n_clicks.index(max(n_clicks))
    device_id = list(DEVICES.keys())[idx]
    device = DEVICES[device_id]

    return html.Div(
        children=[
            html.H2(f"{device['name']} ({device_id})"),

            dcc.Tabs(
                id="tabs",
                value="overview",
                children=[
                    dcc.Tab(label="Overview", value="overview"),
                    dcc.Tab(label="Data", value="data"),
                    dcc.Tab(label="Actions", value="actions"),
                ],
            ),

            html.Div(id="tab-content", style={"marginTop": "20px"}),
        ]
    )

# -----------------------
# Tab rendering
# -----------------------

@callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
    Input({"type": "device", "index": ALL}, "n_clicks"),
)
def render_tab(tab, n_clicks):
    if not any(n_clicks):
        return ""

    idx = n_clicks.index(max(n_clicks))
    device_id = list(DEVICES.keys())[idx]
    device = DEVICES[device_id]

    if tab == "overview":
        return html.Div(
            children=[
                html.P(f"Device ID: {device_id}"),
                html.P(f"RSSI: {device['rssi']} dBm"),
                html.P(f"Battery: {device['battery']} V"),
            ]
        )

    if tab == "data":
        sensor = list(device["sensors"].keys())[0]
        values = device["sensors"][sensor]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                y=values,
                mode="lines+markers",
                name=sensor,
            )
        )
        fig.update_layout(title=f"{sensor} data")

        return dcc.Graph(figure=fig)

    if tab == "actions":
        return html.Div(
            children=[
                html.Button("Toggle LED", id="toggle-led"),
                html.Div(id="action-log"),
            ]
        )

# -----------------------
# Action handling
# -----------------------

@callback(
    Output("action-log", "children"),
    Input("toggle-led", "n_clicks"),
)
def handle_action(n):
    if not n:
        raise exceptions.PreventUpdate
    return f"LED toggled at {time.strftime('%H:%M:%S')}"

if __name__ == "__main__":
    app.run(debug=True)
