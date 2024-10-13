import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash.dash_table as dt
import plotly.graph_objs as go
import pandas as pd
import datetime

app = dash.Dash(__name__)

# Sample data generation
def generate_data(num_points=10, start_time="2024-10-01 00:00"):
    base_time = pd.to_datetime(start_time)
    time_intervals = pd.date_range(base_time, periods=num_points, freq="20T")
    fineness_values = [1, 3, 5, 7, 4, 6, 2, 8, 5, 3][:num_points]

    # Create DataFrame and format time
    data = pd.DataFrame({"Time": time_intervals, "Model Prediction": fineness_values})
    data['Time'] = data['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')  # Format date and time
    
    # Initially, User Prediction is set to Model Prediction
    data['User Prediction'] = data['Model Prediction']
    
    # Reverse the order so the most recent data comes first
    data = data[::-1].reset_index(drop=True)
    
    return data


# Initial data for each graph
data_graph_1 = generate_data()
data_graph_2 = generate_data()
data_graph_3 = generate_data()

# Create graphs
def create_graph(data, title):
    return dcc.Graph(
        id=title,  # Use title as ID for easy reference in callbacks
        figure=go.Figure(
            data=[go.Scatter(x=data["Time"], y=data["User Prediction"], mode='lines+markers')],
            layout=go.Layout(title=title, xaxis_title='Time', yaxis_title='Fineness (1-8)')
        )
    )

# Create tables with dropdown for editing predictions and date/time
def create_table(data, table_id):
    return dt.DataTable(
        id=table_id,
        data=data.to_dict('records'),
        columns=[
            {"name": "Date and Time", "id": "Time", "editable": True},
            {"name": "Model Prediction", "id": "Model Prediction"},
            {"name": "User Prediction", "id": "User Prediction", "editable": True, "presentation": "dropdown"},
        ],
        editable=True,
        dropdown={
            'User Prediction': {
                'options': [{'label': str(i), 'value': i} for i in range(1, 9)]  # Fineness range 1-8
            }
        },
        page_size=5,  # Show only the 5 most recent plots
    )

# Layout
app.layout = html.Div([
    html.H1("Fineness Over Time"),

    # Graph 1 and Table 1 with button
    html.Div([
        html.H2("SNP 1"),
        create_graph(data_graph_1, "graph-1"),
        create_table(data_graph_1.tail(5), "table-1"),
        html.Button("Capture Image for SNP 1", id="btn-snp1", n_clicks=0),
        html.Div(id="output-snp1")
    ]),

    # Graph 2 and Table 2 with button
    html.Div([
        html.H2("SNP 2"),
        create_graph(data_graph_2, "graph-2"),
        create_table(data_graph_2.tail(5), "table-2"),
        html.Button("Capture Image for SNP 2", id="btn-snp2", n_clicks=0),
        html.Div(id="output-snp2")
    ]),

    # Graph 3 and Table 3 with button
    html.Div([
        html.H2("SNP 3"),
        create_graph(data_graph_3, "graph-3"),
        create_table(data_graph_3.tail(5), "table-3"),
        html.Button("Capture Image for SNP 3", id="btn-snp3", n_clicks=0),
        html.Div(id="output-snp3")
    ])
])

# Callbacks to update each graph based on table input
@app.callback(
    Output('graph-1', 'figure'),
    Input('table-1', 'data')
)
def update_graph_1(rows):
    df = pd.DataFrame(rows)
    return go.Figure(
        data=[go.Scatter(x=df["Time"], y=df["User Prediction"], mode='lines+markers')],
        layout=go.Layout(title="SNP 1", xaxis_title='Time', yaxis_title='Fineness (1-8)')
    )

@app.callback(
    Output('graph-2', 'figure'),
    Input('table-2', 'data')
)
def update_graph_2(rows):
    df = pd.DataFrame(rows)
    return go.Figure(
        data=[go.Scatter(x=df["Time"], y=df["User Prediction"], mode='lines+markers')],
        layout=go.Layout(title="SNP 2", xaxis_title='Time', yaxis_title='Fineness (1-8)')
    )

@app.callback(
    Output('graph-3', 'figure'),
    Input('table-3', 'data')
)
def update_graph_3(rows):
    df = pd.DataFrame(rows)
    return go.Figure(
        data=[go.Scatter(x=df["Time"], y=df["User Prediction"], mode='lines+markers')],
        layout=go.Layout(title="SNP 3", xaxis_title='Time', yaxis_title='Fineness (1-8)')
    )

# Callbacks for buttons to add a new row
@app.callback(
    Output("table-1", "data"),
    Input("btn-snp1", "n_clicks"),
    State("table-1", "data")
)
def capture_image_snp1(n_clicks, table_data):
    if n_clicks > 0:
        # Add a new row with current time and model prediction
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_row = {"Time": current_time, "Model Prediction": 5, "User Prediction": 5}
        table_data.insert(0, new_row)  # Insert the new row at the top
    return table_data

@app.callback(
    Output("table-2", "data"),
    Input("btn-snp2", "n_clicks"),
    State("table-2", "data")
)
def capture_image_snp2(n_clicks, table_data):
    if n_clicks > 0:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_row = {"Time": current_time, "Model Prediction": 5, "User Prediction": 5}
        table_data.insert(0, new_row)  # Insert the new row at the top
    return table_data

@app.callback(
    Output("table-3", "data"),
    Input("btn-snp3", "n_clicks"),
    State("table-3", "data")
)
def capture_image_snp3(n_clicks, table_data):
    if n_clicks > 0:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_row = {"Time": current_time, "Model Prediction": 5, "User Prediction": 5}
        table_data.insert(0, new_row)  # Insert the new row at the top
    return table_data

if __name__ == '__main__':
    app.run_server(debug=True)
