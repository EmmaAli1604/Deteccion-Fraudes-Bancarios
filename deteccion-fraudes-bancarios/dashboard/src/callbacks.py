import math
import random

from dash import Input, Output
import plotly.graph_objects as go

from .app import app


# ── Helpers de figura (mismos parámetros que layout.py) ───────

_BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="'DM Mono', monospace", color="#7fa8cc", size=11),
    margin=dict(l=8, r=8, t=8, b=8),
    showlegend=False,
)


def _line_chart(color: str = "#378ADD", anomaly: bool = False) -> go.Figure:
    x = list(range(60))
    y = [50 + 20 * math.sin(i / 8) + random.uniform(-5, 5) for i in x]

    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    traces = [
        go.Scatter(
            x=x, y=y,
            mode="lines",
            line=dict(color=color, width=1.5),
            fill="tozeroy",
            fillcolor=f"rgba({r},{g},{b},0.08)",
            name="serie",
        )
    ]
    if anomaly:
        ax, ay = 42, y[42] + 35
        traces.append(go.Scatter(
            x=[ax], y=[ay],
            mode="markers",
            marker=dict(
                color="#E24B4A", size=10, symbol="x-thin-open",
                line=dict(width=2, color="#E24B4A"),
            ),
            name="anomalía",
        ))

    return go.Figure(
        data=traces,
        layout={
            **_BASE_LAYOUT,
            "xaxis": dict(showgrid=False, zeroline=False, showticklabels=False),
            "yaxis": dict(showgrid=True, gridcolor="rgba(55,138,221,0.08)", zeroline=False),
        },
    )


# ── Registro de callbacks ──────────────────────────────────────

def register_callbacks() -> None:
    """Registra todos los callbacks en la instancia `app`."""

    @app.callback(
        Output("grafico-principal", "figure"),
        Input("filtro-datos", "value"),
    )
    def actualizar_grafico_principal(filtro: str) -> go.Figure:
        """
        Actualiza la serie temporal según el filtro del Dropdown.
            A → transacciones normales (azul)
            B → transacciones sospechosas (rojo + marcador de anomalía)
        """
        if filtro == "B":
            return _line_chart(color="#E24B4A", anomaly=True)
        return _line_chart(color="#378ADD", anomaly=False)