# app.py
from dash import Dash, html, dcc, Input, Output, ALL
import plotly.graph_objs as go
import random
import time
import dash

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
# App setup
# -----------------------
app = Dash(__name__, suppress_callback_exceptions=True)

# -----------------------
# Sidebar generator
# -----------------------
def render_sidebar(updated_names=None):
    if updated_names:
        for device_id, name in zip(DEVICES.keys(), updated_names):
            DEVICES[device_id]['name'] = name

    return html.Div(
        children=[
            html.H3("Devices", style={"marginBottom": "10px"}),
            html.Ul(
                children=[
                    html.Li(
                        f"{device_id} – {DEVICES[device_id]['name']}",
                        id={"type": "device", "index": device_id},
                        n_clicks=0,
                        style={
                            "cursor": "pointer",
                            "whiteSpace": "nowrap",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "padding": "6px 0",
                        },
                    )
                    for device_id in DEVICES
                ],
                style={
                    "listStyleType": "none",
                    "margin": 0,
                    "padding": 0,
                }
            ),
        ],
        style={
            "width": "250px",
            "borderRight": "1px solid #ddd",
            "padding": "10px",
            "overflowY": "auto",
            "height": "100vh",
        },
    )

# -----------------------
# App layout
# -----------------------
app.layout = html.Div(
    children=[
        html.Div(id="sidebar-container", children=render_sidebar()),
        html.Div(
            id="main",
            children=[html.H2("Select a device")],
            style={"width": "75%", "padding": "20px"},
        ),
        dcc.Store(id="selected-device", data=None),
    ],
    style={"display": "flex"},
)

# -----------------------
# Device selection callback
# -----------------------
@app.callback(
    Output("main", "children"),
    Output("selected-device", "data"),
    Input({"type": "device", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def select_device(n_clicks):
    if not any(n_clicks):
        raise dash.exceptions.PreventUpdate

    idx = n_clicks.index(max(n_clicks))
    device_id = list(DEVICES.keys())[idx]
    device = DEVICES[device_id]

    layout = html.Div(
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
            # Separate divs per tab
            html.Div(id="overview-content", style={"marginTop": "20px"}),
            html.Div(id="data-content", style={"marginTop": "20px"}),
            html.Div(id="actions-content", style={"marginTop": "20px"}),
        ]
    )

    return layout, device_id

# -----------------------
# Tab content callback
# -----------------------
@app.callback(
    Output("sensor-graph", "figure"),
    Input("sensor-dropdown", "value"),
    Input("selected-device", "data"),
)
def update_sensor_graph(selected_sensor, device_id):
    if not device_id or not selected_sensor:
        return go.Figure()  # empty graph

    device = DEVICES[device_id]
    values = device["sensors"][selected_sensor]

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=values, mode="lines+markers", name=selected_sensor))
    fig.update_layout(title=f"{selected_sensor} data")
    return fig


@app.callback(
    Output("overview-content", "children"),
    Output("data-content", "children"),
    Output("actions-content", "children"),
    Input("tabs", "value"),
    Input("selected-device", "data"),
)
def render_tabs(tab, device_id):
    if not device_id:
        return html.P("Select a device"), None, None

    device = DEVICES[device_id]

    # Overview tab
    overview_layout = html.Div(
        children=[
            html.P(f"Device ID: {device_id}"),
            html.Div([
                html.Label("Device Name: "),
                dcc.Input(
                    id={"type": "device-name-input", "index": device_id},
                    value=device['name'],
                    type="text",
                    debounce=True
                ),
            ]),
            html.P(f"RSSI: {device['rssi']} dBm"),
            html.P(f"Battery: {device['battery']} V"),
        ]
    ) if tab == "overview" else None

    # Data tab
    if tab == "data":
        sensors = list(device["sensors"].keys())
        
        data_layout = html.Div([
            html.Label("Select Sensor:"),
            dcc.Dropdown(
                id="sensor-dropdown",
                options=[{"label": s, "value": s} for s in sensors],
                value=sensors[0],
                clearable=False,
                style={"width": "200px", "marginBottom": "10px"},
            ),
            dcc.Graph(id="sensor-graph")
        ])
    else:
        data_layout = None


    # Actions tab
    actions_layout = html.Div([
        html.Button("Toggle LED", id="toggle-led"),
        html.Div(id="action-log"),
    ]) if tab == "actions" else None

    return overview_layout, data_layout, actions_layout

# -----------------------
# Device name input callback
# -----------------------
@app.callback(
    Output("sidebar-container", "children"),
    Input({"type": "device-name-input", "index": ALL}, "value"),
)
def update_sidebar(updated_names):
    return render_sidebar(updated_names)

# -----------------------
# Action button callback
# -----------------------
@app.callback(
    Output("action-log", "children"),
    Input("toggle-led", "n_clicks"),
    prevent_initial_call=True
)
def handle_action(n):
    return f"LED toggled at {time.strftime('%H:%M:%S')}"

# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)

