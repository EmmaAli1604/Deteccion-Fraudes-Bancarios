import math
import random

import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go

from components import content_card, kpi_card

# ────────────────────────────────────────────────────────────
# Constantes de estilo Plotly
# ────────────────────────────────────────────────────────────

PLOT_CONFIG = {"displayModeBar": False, "responsive": True}

TRANSPARENT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono, monospace", color="#7fa8cc", size=11),
    margin=dict(l=8, r=8, t=8, b=8),
)

# Opciones del Dropdown heredadas del documento original
FILTRO_OPTIONS = [
    {"label": "Opción A — Transacciones normales", "value": "A"},
    {"label": "Opción B — Transacciones sospechosas", "value": "B"},
]

# ────────────────────────────────────────────────────────────
# Helpers: generadores de figuras Plotly
# ────────────────────────────────────────────────────────────

def _line_chart(color: str = "#2f80ed", anomaly: bool = False) -> go.Figure:
    """Serie temporal con punto de anomalía opcional."""
    x = list(range(60))
    y = [50 + 20 * math.sin(i / 8) + random.uniform(-5, 5) for i in x]

    traces = [
        go.Scatter(
            x=x, y=y,
            mode="lines",
            line=dict(color=color, width=1.5),
            fill="tozeroy",
            fillcolor=(
                f"rgba({int(color[1:3],16)},"
                f"{int(color[3:5],16)},"
                f"{int(color[5:7],16)},0.08)"
            ),
            name="serie",
        )
    ]

    if anomaly:
        ax, ay = 42, y[42] + 35
        traces.append(go.Scatter(
            x=[ax], y=[ay],
            mode="markers",
            marker=dict(
                color="#e63946", size=10, symbol="x-thin-open",
                line=dict(width=2, color="#e63946"),
            ),
            name="anomalía",
        ))

    return go.Figure(
        data=traces,
        layout={
            **TRANSPARENT_LAYOUT,
            "xaxis": dict(showgrid=False, zeroline=False, showticklabels=False),
            "yaxis": dict(showgrid=True, gridcolor="rgba(47,128,237,0.08)", zeroline=False),
            "showlegend": False,
        },
    )


def _bar_chart(color: str = "#2f80ed") -> go.Figure:
    cats = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]
    vals = [12, 18, 45, 72, 60, 30]
    colors = [color if v < 65 else "#e63946" for v in vals]

    return go.Figure(
        go.Bar(x=cats, y=vals, marker_color=colors, marker_line_width=0),
        layout={
            **TRANSPARENT_LAYOUT,
            "xaxis": dict(showgrid=False, zeroline=False),
            "yaxis": dict(showgrid=True, gridcolor="rgba(47,128,237,0.08)", zeroline=False),
        },
    )


def _scatter_chart() -> go.Figure:
    x = [random.gauss(0, 1) for _ in range(80)]
    y = [random.gauss(0, 1) for _ in range(80)]
    c = ["#e63946" if abs(xi) > 2 or abs(yi) > 2 else "#2f80ed"
         for xi, yi in zip(x, y)]

    return go.Figure(
        go.Scatter(x=x, y=y, mode="markers",
                   marker=dict(color=c, size=6, opacity=0.8)),
        layout={
            **TRANSPARENT_LAYOUT,
            "xaxis": dict(showgrid=True, gridcolor="rgba(47,128,237,0.08)", zeroline=False),
            "yaxis": dict(showgrid=True, gridcolor="rgba(47,128,237,0.08)", zeroline=False),
        },
    )


def _grafico_principal(filtro: str) -> go.Figure:
    """
    Figura reactiva conectada al Dropdown 'filtro-datos'.
    Opción A → serie normal (azul).
    Opción B → serie con anomalías (rojo).
    """
    if filtro == "B":
        return _line_chart(color="#e63946", anomaly=True)
    return _line_chart(color="#2f80ed", anomaly=False)


def graph(fig: go.Figure, height: int = 200) -> dcc.Graph:
    return dcc.Graph(
        figure=fig,
        config=PLOT_CONFIG,
        style={"height": f"{height}px", "width": "100%"},
    )


# ────────────────────────────────────────────────────────────
# serve_layout  ← patrón del documento original
# ────────────────────────────────────────────────────────────

def serve_layout() -> html.Div:
    """
    Construye y retorna el layout completo del dashboard.
    Llamar app.layout = serve_layout  (sin paréntesis) hace que
    Dash regenere el layout en cada carga de página.
    """

    # ── FILA 1: 5 KPI Cards ──────────────────────────────────
    kpi_row = html.Div(
        className="dash-section",
        children=[
            html.Div("— Indicadores clave", className="dash-section__label"),
            html.Div(
                className="kpi-grid",
                children=[
                    kpi_card(
                        card_id="kpi-1",
                        label="Anomalías detectadas",
                        value="23",
                        delta="▲ +7 vs. ayer",
                        icon="🔴",
                        bar_pct=78,
                        status="danger",
                    ),
                    kpi_card(
                        card_id="kpi-2",
                        label="Latencia P95",
                        value="142 ms",
                        delta="▲ +18 ms",
                        icon="⚡",
                        bar_pct=62,
                        status="warn",
                    ),
                    kpi_card(
                        card_id="kpi-3",
                        label="Tasa de error",
                        value="0.8 %",
                        delta="▼ −0.1 %",
                        icon="✓",
                        bar_pct=20,
                        status="normal",
                    ),
                    kpi_card(
                        card_id="kpi-4",
                        label="Throughput",
                        value="4.2 k/s",
                        delta="▲ +300/s",
                        icon="📈",
                        bar_pct=55,
                        status="normal",
                    ),
                    kpi_card(
                        card_id="kpi-5",
                        label="Score de riesgo",
                        value="87 / 100",
                        delta="▲ crítico",
                        icon="⚠",
                        bar_pct=87,
                        status="danger",
                    ),
                ],
            ),
        ],
    )

    # ── FILA 2: Filtro + gráfico principal (del documento original) ──
    filtro_row = html.Div(
        className="dash-section",
        children=[
            html.Div("— Análisis exploratorio de transacciones", className="dash-section__label"),
            html.Div(
                className="asymmetric-grid",
                children=[
                    # Card ancha: título heredado del documento original
                    content_card(
                        card_id="card-principal",
                        title="Análisis Exploratorio de Transacciones",
                        badge="INTERACTIVO",
                        badge_status="normal",
                        wide=True,
                        status="normal",
                        children=[
                            # ── Dropdown del documento original ──────
                            dcc.Dropdown(
                                id="filtro-datos",          # ← id original conservado
                                options=FILTRO_OPTIONS,
                                value="A",
                                clearable=False,
                                style={
                                    "marginBottom": "12px",
                                    "fontFamily": "var(--font-display)",
                                    "fontSize": "12px",
                                    "backgroundColor": "var(--bg-panel)",
                                    "color": "var(--text-primary)",
                                    "border": "1px solid var(--border-mid)",
                                    "borderRadius": "var(--radius-sm)",
                                },
                            ),
                            # ── Gráfico principal del documento original ──
                            dcc.Graph(
                                id="grafico-principal",     # ← id original conservado
                                config=PLOT_CONFIG,
                                style={"height": "180px", "width": "100%"},
                            ),
                        ],
                    ),
                    # Card derecha superior
                    content_card(
                        card_id="card-bar-filtro",
                        title="Errores por hora",
                        badge="NORMAL",
                        badge_status="normal",
                        status="normal",
                        children=graph(_bar_chart(color="#2f80ed"), height=240),
                    ),
                    # Card derecha inferior
                    content_card(
                        card_id="card-scatter-filtro",
                        title="Espacio de características",
                        badge="VIGILANCIA",
                        badge_status="warn",
                        status="warn",
                        children=graph(_scatter_chart(), height=240),
                    ),
                ],
            ),
        ],
    )

    # ── FILA 3: Asimétrico ────────────────────────────────────
    row3 = html.Div(
        className="dash-section",
        children=[
            html.Div("— Serie temporal & distribución", className="dash-section__label"),
            html.Div(
                className="asymmetric-grid",
                children=[
                    content_card(
                        card_id="card-serie-1",
                        title="Tráfico de red — últimos 60 min",
                        badge="ANOMALÍA DETECTADA",
                        badge_status="danger",
                        wide=True,
                        status="danger",
                        children=graph(_line_chart(color="#e63946", anomaly=True), height=220),
                    ),
                    content_card(
                        card_id="card-bar-1",
                        title="Monto por categoría",
                        badge="NORMAL",
                        badge_status="normal",
                        status="normal",
                        children=graph(_bar_chart(color="#2f80ed"), height=220),
                    ),
                    content_card(
                        card_id="card-scatter-1",
                        title="Dispersión de montos",
                        badge="VIGILANCIA",
                        badge_status="warn",
                        status="warn",
                        children=graph(_scatter_chart(), height=220),
                    ),
                ],
            ),
        ],
    )

    # ── FILA 4: Asimétrico ────────────────────────────────────
    row4 = html.Div(
        className="dash-section",
        children=[
            html.Div("— Logs & métricas secundarias", className="dash-section__label"),
            html.Div(
                className="asymmetric-grid",
                children=[
                    content_card(
                        card_id="card-serie-2",
                        title="Uso de CPU — clúster principal",
                        badge="ESTABLE",
                        badge_status="normal",
                        wide=True,
                        status="normal",
                        children=graph(_line_chart(color="#2f80ed", anomaly=False), height=220),
                    ),
                    content_card(
                        card_id="card-bar-2",
                        title="Peticiones denegadas",
                        badge="ADVERTENCIA",
                        badge_status="warn",
                        status="warn",
                        children=graph(_bar_chart(color="#f4a621"), height=220),
                    ),
                    content_card(
                        card_id="card-scatter-2",
                        title="Correlación de señales",
                        badge="NORMAL",
                        badge_status="normal",
                        status="normal",
                        children=graph(_scatter_chart(), height=220),
                    ),
                ],
            ),
        ],
    )

    # ── Layout raíz ──────────────────────────────────────────
    return html.Div(
        className="dash-wrapper",
        children=[
            # Header
            html.Div(
                className="dash-header",
                children=[
                    html.Div([
                        html.Div(
                            ["ANOMALY", html.Span(" WATCH"), " — Panel de control"],
                            className="dash-header__title",
                        ),
                        html.Div(
                            "Análisis Exploratorio de Transacciones",   # ← título del doc original
                            className="dash-header__subtitle",
                        ),
                    ]),
                    html.Span("● EN VIVO", className="dash-header__badge badge-live"),
                ],
            ),
            kpi_row,
            filtro_row,
            row3,
            row4,
        ],
    )


# ────────────────────────────────────────────────────────────
# App + Callbacks
# ────────────────────────────────────────────────────────────

app = dash.Dash(__name__, title="Anomaly Dashboard — Transacciones")

# Asignar como función (sin paréntesis) → layout se regenera por request
app.layout = serve_layout


@app.callback(
    Output("grafico-principal", "figure"),   # ← id original conservado
    Input("filtro-datos", "value"),          # ← id original conservado
)
def actualizar_grafico_principal(filtro: str) -> go.Figure:
    """
    Callback conectado al Dropdown del documento original.
    Actualiza 'grafico-principal' según el valor seleccionado.
    """
    return _grafico_principal(filtro)


if __name__ == "__main__":
    app.run(debug=True)