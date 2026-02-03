import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.graph_objs as go
import pandas as pd
import base64
import io
from datetime import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("ECU Log Data Analyzer", style={'textAlign': 'center', 'marginBottom': 30}),
    
    # File upload section
    html.Div([
        html.H3("Upload ECU Log CSV File"),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                'backgroundColor': '#f9f9f9'
            },
            multiple=False
        ),
        html.Div(id='upload-status', style={'margin': '10px'})
    ], style={'marginBottom': 30}),
    
    # Data info section
    html.Div(id='data-info', style={'marginBottom': 20}),
    
    # Field selection section
    html.Div([
        html.H3("Select Fields to Plot"),
        html.Div([
            html.Label("Y-Axis Fields (Left):"),
            dcc.Dropdown(
                id='y-fields-left',
                multi=True,
                placeholder="Select fields for left Y-axis"
            )
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
        
        html.Div([
            html.Label("Y-Axis Fields (Right):"),
            dcc.Dropdown(
                id='y-fields-right',
                multi=True,
                placeholder="Select fields for right Y-axis (optional)"
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            html.Label("X-Axis Field:"),
            dcc.Dropdown(
                id='x-field',
                placeholder="Select X-axis field (default: Time)"
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.Label("Filter by Time Range:"),
            html.Br(),
            dcc.RangeSlider(
                id='time-range-slider',
                min=0,
                max=100,
                value=[0, 100],
                marks={},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={'width': '60%', 'display': 'inline-block', 'marginTop': '10px'})
        
    ], id='field-selection', style={'display': 'none', 'marginBottom': 30}),
    
    # Plot controls
    html.Div([
        html.Button('Update Plot', id='update-plot-btn', n_clicks=0, 
                   style={'backgroundColor': '#007bff', 'color': 'white', 'padding': '10px 20px', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'}),
        html.Button('Clear Plot', id='clear-plot-btn', n_clicks=0, 
                   style={'backgroundColor': '#dc3545', 'color': 'white', 'padding': '10px 20px', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'marginLeft': '10px'})
    ], id='plot-controls', style={'display': 'none', 'marginBottom': 20}),
    
    # Graph section
    dcc.Graph(id='ecu-graph', style={'height': '600px'}),
    
    # Data table section (optional)
    html.Div([
        html.H3("Data Summary"),
        html.Div(id='data-table')
    ], id='data-summary', style={'display': 'none', 'marginTop': 30}),
    
    # Store component to hold the data
    dcc.Store(id='stored-data')
])

def parse_contents(contents, filename):
    """Parse uploaded CSV file"""
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            return None, "Please upload a CSV file"
    except Exception as e:
        return None, f"Error reading file: {str(e)}"
    
    return df, None

@app.callback(
    [Output('stored-data', 'data'),
     Output('upload-status', 'children'),
     Output('field-selection', 'style'),
     Output('plot-controls', 'style'),
     Output('data-summary', 'style'),
     Output('data-info', 'children')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(contents, filename):
    if contents is None:
        return None, "", {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, ""
    
    df, error = parse_contents(contents, filename)
    
    if error:
        return None, html.Div([html.H5("Error:", style={'color': 'red'}), error]), {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, ""
    
    # Data info
    data_info = html.Div([
        html.H4("Data Summary:"),
        html.P(f"File: {filename}"),
        html.P(f"Rows: {len(df)}, Columns: {len(df.columns)}"),
        html.P(f"Columns: {', '.join(df.columns[:10])}{'...' if len(df.columns) > 10 else ''}")
    ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '5px'})
    
    return (df.to_dict('records'), 
            html.Div([html.H5("Success!", style={'color': 'green'}), f"Loaded {filename} with {len(df)} rows"]),
            {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, data_info)

@app.callback(
    [Output('y-fields-left', 'options'),
     Output('y-fields-right', 'options'),
     Output('x-field', 'options'),
     Output('x-field', 'value'),
     Output('time-range-slider', 'min'),
     Output('time-range-slider', 'max'),
     Output('time-range-slider', 'marks')],
    [Input('stored-data', 'data')]
)
def update_dropdowns(data):
    if data is None:
        return [], [], [], None, 0, 100, {}
    
    df = pd.DataFrame(data)
    columns = df.columns.tolist()
    
    # Create options for dropdowns
    options = [{'label': col, 'value': col} for col in columns]
    
    # Set default X-axis to Time if available
    default_x = 'Time' if 'Time' in columns else columns[0] if columns else None
    
    # Setup time range slider
    if default_x and default_x in df.columns:
        x_min, x_max = 0, len(df) - 1
        marks = {
            0: str(df[default_x].iloc[0]) if len(df) > 0 else '0',
            len(df) - 1: str(df[default_x].iloc[-1]) if len(df) > 0 else str(len(df))
        }
    else:
        x_min, x_max, marks = 0, 100, {0: '0', 100: '100'}
    
    return options, options, options, default_x, x_min, x_max, marks

@app.callback(
    Output('ecu-graph', 'figure'),
    [Input('update-plot-btn', 'n_clicks'),
     Input('clear-plot-btn', 'n_clicks')],
    [State('stored-data', 'data'),
     State('y-fields-left', 'value'),
     State('y-fields-right', 'value'),
     State('x-field', 'value'),
     State('time-range-slider', 'value')]
)
def update_graph(update_clicks, clear_clicks, data, y_left, y_right, x_field, time_range):
    ctx = callback_context
    
    if not ctx.triggered:
        # Return empty plot initially
        return go.Figure()
    
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger == 'clear-plot-btn':
        return go.Figure()
    
    if data is None or not y_left:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # Apply time range filter
    if time_range:
        start_idx, end_idx = int(time_range[0]), int(time_range[1])
        df = df.iloc[start_idx:end_idx+1]
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Set x-axis data
    x_data = df[x_field] if x_field else df.index
    
    # Color palette for lines
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    # Add left y-axis traces
    for i, field in enumerate(y_left):
        if field in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=df[field],
                    mode='lines',
                    name=field,
                    line=dict(color=colors[i % len(colors)]),
                    yaxis='y'
                )
            )
    
    # Add right y-axis traces
    if y_right:
        for i, field in enumerate(y_right):
            if field in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=x_data,
                        y=df[field],
                        mode='lines',
                        name=f"{field} (R)",
                        line=dict(color=colors[(len(y_left) + i) % len(colors)], dash='dash'),
                        yaxis='y2'
                    )
                )
    
    # Update layout
    fig.update_layout(
        title="ECU Log Data Analysis",
        xaxis_title=x_field or "Index",
        yaxis=dict(
            title="Left Y-Axis",
            side="left"
        ),
        yaxis2=dict(
            title="Right Y-Axis",
            side="right",
            overlaying="y"
        ) if y_right else None,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=600
    )
    
    return fig

@app.callback(
    Output('data-table', 'children'),
    [Input('stored-data', 'data'),
     Input('y-fields-left', 'value'),
     State('time-range-slider', 'value')]
)
def update_data_summary(data, selected_fields, time_range):
    if data is None or not selected_fields:
        return "Upload data and select fields to see summary statistics."
    
    df = pd.DataFrame(data)
    
    # Apply time range filter
    if time_range:
        start_idx, end_idx = int(time_range[0]), int(time_range[1])
        df = df.iloc[start_idx:end_idx+1]
    
    # Create summary statistics for selected fields
    summary_data = []
    for field in selected_fields:
        if field in df.columns:
            stats = df[field].describe()
            summary_data.append({
                'Field': field,
                'Count': f"{stats['count']:.0f}",
                'Mean': f"{stats['mean']:.2f}",
                'Std': f"{stats['std']:.2f}",
                'Min': f"{stats['min']:.2f}",
                'Max': f"{stats['max']:.2f}"
            })
    
    if not summary_data:
        return "No valid fields selected."
    
    # Create a simple table
    table_rows = []
    # Header
    table_rows.append(html.Tr([
        html.Th(col) for col in ['Field', 'Count', 'Mean', 'Std Dev', 'Min', 'Max']
    ]))
    # Data rows
    for row in summary_data:
        table_rows.append(html.Tr([
            html.Td(row[col]) for col in ['Field', 'Count', 'Mean', 'Std', 'Min', 'Max']
        ]))
    
    return html.Table(table_rows, style={'width': '100%', 'border': '1px solid black'})

if __name__ == '__main__':
    app.run(debug=True)