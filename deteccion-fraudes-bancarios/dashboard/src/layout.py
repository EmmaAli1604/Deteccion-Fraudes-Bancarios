import math
import random

from dash import dcc, html
import plotly.graph_objects as go

from .utils import content_card, kpi_card


# ── Configuración global de gráficas ──────────────────────────

PLOT_CONFIG = {"displayModeBar": False, "responsive": True}

_BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="'DM Mono', monospace", color="#7fa8cc", size=11),
    margin=dict(l=8, r=8, t=8, b=8),
    showlegend=False,
)

FILTRO_OPTIONS = [
    {"label": "Opción A — Transacciones normales",      "value": "A"},
    {"label": "Opción B — Transacciones sospechosas",   "value": "B"},
]


# ── Helpers: figuras Plotly ────────────────────────────────────

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


def _bar_chart(color: str = "#378ADD") -> go.Figure:
    cats = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]
    vals = [12, 18, 45, 72, 60, 30]
    colors = [color if v < 65 else "#E24B4A" for v in vals]

    return go.Figure(
        go.Bar(x=cats, y=vals, marker_color=colors, marker_line_width=0),
        layout={
            **_BASE_LAYOUT,
            "xaxis": dict(showgrid=False, zeroline=False),
            "yaxis": dict(showgrid=True, gridcolor="rgba(55,138,221,0.08)", zeroline=False),
        },
    )


def _scatter_chart() -> go.Figure:
    x = [random.gauss(0, 1) for _ in range(80)]
    y = [random.gauss(0, 1) for _ in range(80)]
    c = ["#E24B4A" if abs(xi) > 2 or abs(yi) > 2 else "#378ADD"
         for xi, yi in zip(x, y)]

    return go.Figure(
        go.Scatter(x=x, y=y, mode="markers",
                   marker=dict(color=c, size=6, opacity=0.8)),
        layout={
            **_BASE_LAYOUT,
            "xaxis": dict(showgrid=True, gridcolor="rgba(55,138,221,0.08)", zeroline=False),
            "yaxis": dict(showgrid=True, gridcolor="rgba(55,138,221,0.08)", zeroline=False),
        },
    )


def _graph(fig: go.Figure, height: int = 200) -> dcc.Graph:
    return dcc.Graph(
        figure=fig,
        config=PLOT_CONFIG,
        style={"height": f"{height}px", "width": "100%"},
    )


# ── serve_layout ───────────────────────────────────────────────

def serve_layout() -> html.Div:
    """
    Construye y retorna el layout completo.
    Dash regenera el layout en cada carga de página cuando se asigna
    como función:  app.layout = serve_layout  (sin paréntesis).
    En main.py se llama con paréntesis para asignación estática.
    """

    # ── HEADER ──────────────────────────────────────────────
    header = html.Header(
        className="dash-header",
        children=[
            html.Div(className="dash-header__left", children=[
                html.Div(
                    children=[
                        "Análisis de Exploratorio de Transacciones",
                    ],
                    className="dash-header__title",
                    html_sub="FILAS :  6362620 , COLUMNAS :  11",
                ),
            ]),
        ],
    )

    # ── FILA 1: KPIs ────────────────────────────────────────
    kpi_row = html.Section(
        className="dash-section",
        children=[
            html.P("Indicadores clave", className="section-label"),
            html.Div(
                className="kpi-grid",
                children=[
                    kpi_card(
                        card_id="kpi-1",
                        label="Total de transacciones",
                        # Aqui va total de transacciones
                        value="",
                    ),
                    kpi_card(
                        card_id="kpi-2",
                        label="Porcentaje de Fraudes",
                        # Aqui va porcentaje de fraudes
                        value="",
                    ),
                    kpi_card(
                        card_id="kpi-3",
                        label="Monto Más Común",
                        # Aqui va el monto mas comun
                        value="",
                    ),
                    kpi_card(
                        card_id="kpi-4",
                        label="Indice de Gini",
                        # Aqui va el indice de gini
                        value="",
                    ),
                    kpi_card(
                        card_id="kpi-5",
                        label="Desviación Estándar de Montos",
                    ),
                ],
            ),
        ],
    )

    # ── FILA 2: Análisis exploratorio (con dropdown reactivo) ──
    filtro_row = html.Section(
        className="dash-section",
        children=[
            html.P("Análisis exploratorio de transacciones", className="section-label"),
            html.Div(
                className="asymmetric-grid",
                children=[
                    content_card(
                        card_id="card-principal",
                        title="Serie temporal de transacciones",
                        badge="Interactivo",
                        badge_status="normal",
                        wide=True,
                        status="normal",
                        children=[
                            dcc.Dropdown(
                                id="filtro-datos",
                                options=FILTRO_OPTIONS,
                                value="A",
                                clearable=False,
                                className="dash-dropdown",
                            ),
                            dcc.Graph(
                                id="grafico-principal",
                                config=PLOT_CONFIG,
                                style={"height": "180px", "width": "100%"},
                            ),
                        ],
                    ),
                    content_card(
                        card_id="card-bar-filtro",
                        title="Errores por hora",
                        badge="Normal",
                        badge_status="normal",
                        status="normal",
                        children=_graph(_bar_chart(color="#378ADD"), height=240),
                    ),
                    content_card(
                        card_id="card-scatter-filtro",
                        title="Espacio de características",
                        badge="Vigilancia",
                        badge_status="warn",
                        status="warn",
                        children=_graph(_scatter_chart(), height=240),
                    ),
                ],
            ),
        ],
    )

    # ── FILA 3: Serie temporal & dispersión ────────────────
    row3 = html.Section(
        className="dash-section",
        children=[
            html.P("Serie temporal & distribución", className="section-label"),
            html.Div(
                className="asymmetric-grid",
                children=[
                    content_card(
                        card_id="card-serie-1",
                        title="Tráfico de red — últimos 60 min",
                        badge="Anomalía detectada",
                        badge_status="danger",
                        wide=True,
                        status="danger",
                        children=_graph(_line_chart(color="#E24B4A", anomaly=True), height=220),
                    ),
                    content_card(
                        card_id="card-bar-1",
                        title="Monto por categoría",
                        badge="Normal",
                        badge_status="normal",
                        status="normal",
                        children=_graph(_bar_chart(color="#378ADD"), height=220),
                    ),
                    content_card(
                        card_id="card-scatter-1",
                        title="Dispersión de montos",
                        badge="Vigilancia",
                        badge_status="warn",
                        status="warn",
                        children=_graph(_scatter_chart(), height=220),
                    ),
                ],
            ),
        ],
    )

    # ── FILA 4: Logs & métricas secundarias ────────────────
    row4 = html.Section(
        className="dash-section",
        children=[
            html.P("Logs & métricas secundarias", className="section-label"),
            html.Div(
                className="asymmetric-grid",
                children=[
                    content_card(
                        card_id="card-serie-2",
                        title="Uso de CPU — clúster principal",
                        badge="Estable",
                        badge_status="normal",
                        wide=True,
                        status="normal",
                        children=_graph(_line_chart(color="#378ADD", anomaly=False), height=220),
                    ),
                    content_card(
                        card_id="card-bar-2",
                        title="Peticiones denegadas",
                        badge="Advertencia",
                        badge_status="warn",
                        status="warn",
                        children=_graph(_bar_chart(color="#BA7517"), height=220),
                    ),
                    content_card(
                        card_id="card-scatter-2",
                        title="Correlación de señales",
                        badge="Normal",
                        badge_status="normal",
                        status="normal",
                        children=_graph(_scatter_chart(), height=220),
                    ),
                ],
            ),
        ],
    )
    
    footer = html.Footer(
        className="dash-footer",
        children=[
            html.Span("Fuente del dataset: ", className="dash-footer__label"),
            html.A(
                "Fraud Detection Dynamics — Financial Transactions (Kaggle)",
                href="https://www.kaggle.com/datasets/rohit265/fraud-detection-dynamics-financial-transaction",
                target="_blank",
                rel="noopener noreferrer",
                className="dash-footer__link",
            ),
            html.Span(" · Extraído el 01/06/2026", className="dash-footer__date"),
        ],
    )

    # ── Root ──────────────────────────────────────────────
    return html.Div(
        className="dash-wrapper",
        children=[header, kpi_row, filtro_row, row3, row4],
    )