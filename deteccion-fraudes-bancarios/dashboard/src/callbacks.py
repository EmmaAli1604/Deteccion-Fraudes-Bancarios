from dash import Input, Output
from src.app import app
import plotly.express as px
import pandas as pd

def register_callbacks():
    @app.callback(
        Output('grafico-principal', 'figure'),
        Input('filtro-datos', 'value')
    )
    def actualizar_grafico(seleccion):
        df = pd.DataFrame({'Eje X': [1, 2, 3], 'Eje Y': [4, 1, 2]})
        fig = px.line(df, x='Eje X', y='Eje Y', title=f"Viendo: {seleccion}")
        return fig