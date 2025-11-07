"""
Dashboard Dash para visualização de métricas ML.
"""
import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("ML & Big Data Dashboard"),
    
    html.Div([
        html.Div([
            dcc.Graph(id='model-performance')
        ], className='six columns'),
        
        html.Div([
            dcc.Graph(id='prediction-distribution')
        ], className='six columns'),
    ], className='row'),
    
    html.Div([
        dcc.Graph(id='data-overview')
    ], className='row'),
    
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Atualiza a cada minuto
        n_intervals=0
    )
])


@app.callback(
    dash.dependencies.Output('model-performance', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_model_performance(n):
    """Atualiza gráfico de performance do modelo."""
    # Exemplo de dados
    data = {
        'model': ['Random Forest', 'Gradient Boosting', 'Logistic Regression'],
        'accuracy': [0.95, 0.93, 0.88],
        'f1_score': [0.94, 0.92, 0.87]
    }
    df = pd.DataFrame(data)
    
    fig = go.Figure(data=[
        go.Bar(name='Accuracy', x=df['model'], y=df['accuracy']),
        go.Bar(name='F1 Score', x=df['model'], y=df['f1_score'])
    ])
    
    fig.update_layout(
        title='Model Performance',
        barmode='group'
    )
    
    return fig


@app.callback(
    dash.dependencies.Output('prediction-distribution', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_prediction_distribution(n):
    """Atualiza distribuição de predições."""
    # Exemplo de dados
    predictions = np.random.normal(0.5, 0.1, 1000)
    
    fig = go.Figure(data=[go.Histogram(x=predictions)])
    
    fig.update_layout(
        title='Prediction Distribution'
    )
    
    return fig


@app.callback(
    dash.dependencies.Output('data-overview', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_data_overview(n):
    """Atualiza visão geral dos dados."""
    # Exemplo de dados
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    values = pd.Series(range(30)) + pd.Series(np.random.randn(30))
    
    fig = go.Figure(data=[go.Scatter(x=dates, y=values, mode='lines+markers')])
    
    fig.update_layout(
        title='Data Overview - Time Series'
    )
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)

