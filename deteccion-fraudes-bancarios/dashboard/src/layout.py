from dash import html, dcc

def serve_layout():
    return html.Div([
        html.H1("Dashboard de Análisis"),
        dcc.Dropdown(
            id='filtro-datos',
            options=[{'label': 'Opción A', 'value': 'A'}, {'label': 'Opción B', 'value': 'B'}],
            value='A'
        ),
        dcc.Graph(id='grafico-principal')
    ])