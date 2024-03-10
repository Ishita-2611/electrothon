import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Sample data
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 15, 13, 17, 18]
})

# Initialize the Dash app
app = dash.Dash(_name_)

# Define the layout
app.layout = html.Div([
    html.H1('Dashboard'),
    
    dcc.Graph(id='example-graph'),
    
    html.Div([
        html.Label('Select Data Points:'),
        dcc.RangeSlider(
            id='range-slider',
            min=0,
            max=len(df) - 1,
            step=1,
            marks={i: str(i) for i in range(len(df))},
            value=[0, len(df) - 1]
        )
    ]),
    
    html.Div(id='output-div')
])

# Define callback to update the graph based on slider input
@app.callback(
Output('example-graph', 'figure'),
    [Input('range-slider', 'value')]
)
def update_graph(selected_data):
    filtered_df = df.iloc[selected_data[0]:selected_data[1] + 1]
    trace = go.Scatter(x=filtered_df['x'], y=filtered_df['y'], mode='lines+markers')
    return {'data': [trace], 'layout': go.Layout(title='Selected Data Points')}

# Define callback to display selected data points
@app.callback(
    Output('output-div', 'children'),
    [Input('range-slider', 'value')]
)
def display_selected_data(selected_data):
    selected_df = df.iloc[selected_data[0]:selected_data[1] + 1]
    return html.Div([
        html.H3('Selected Data Points:'),
        html.Table([
            html.Tr([html.Th(col) for col in selected_df.columns]),
            *[html.Tr([html.Td(selected_df.iloc[i][col]) for col in selected_df.columns]) for i in range(len(selected_df))]
        ])
    ])

# Run the app
if _name_ == '_main_':
    app.run_server(debug=True)