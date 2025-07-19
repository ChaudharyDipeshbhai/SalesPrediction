import pandas as pd
import dash
import os
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

forecast_df = pd.read_csv('data/Product_12_week_forecast.csv')

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Retail Sales Forecast Dashboard", className= "text-center text-primary my-4"),
    
    dbc.Row([
        dbc.Col([
            html.Label("Select Product Category:"),
            dcc.Dropdown(
                id="category-dropdown",
                options=[{'label': cat, 'value': cat} for cat in forecast_df['ProductCategory'].unique()],
                value= forecast_df['ProductCategory'].unique()[0],
                className = 'mb-4'
            ),
        ], width = 4),
    ], justify = 'center'),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='quantity-forecast-graph'), width=6),
        dbc.Col(dcc.Graph(id='amount-forecast-graph'), width=6),
    ], className='mb-4'),

    dbc.Row([
        dbc.Col([
            html.H4("Forecast Data Table", className='text-center'),
            dash_table.DataTable(
                id='forecast-table',
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'center',
                    'minWidth': '100px', 'width': '150px', 'maxWidth': '180px',
                    'whiteSpace': 'normal'
                },
                style_header={
                    'backgroundColor': 'rgb(30, 30, 30)',
                    'color': 'white'
                },
                style_data={
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'
                }
            )
        ])
    ])
], fluid = True)


#Callbacks

@app.callback(
    [Output('quantity-forecast-graph', 'figure'),
     Output('amount-forecast-graph', 'figure'),
     Output('forecast-table', 'data')],
    [Input('category-dropdown', 'value')]
)
def update_dashboard(selected_category):
    filtered_df = forecast_df[forecast_df['ProductCategory'] == selected_category]
    
    fig_qty = px.line(
        filtered_df, x = 'week_ahead', y= 'Predicted_Quantity',
        title = f'Quantity Forecast for {selected_category}',
        markers = True
    )
    fig_qty.update_layout(template = 'plotly_dark')
    
    fig_amt = px.line(
        filtered_df, x = 'week_ahead' , y = 'Predicted_Amount',
        title= f'Revenue Forecast for {selected_category}',
        markers= True
    )
    fig_amt.update_layout(template = 'plotly_dark')
    
    table_data = filtered_df.to_dict('records')
    
    return fig_qty, fig_amt, table_data

# run server
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))  # Render sets PORT automatically
    app.run(host='0.0.0.0', port=port, debug=True)

