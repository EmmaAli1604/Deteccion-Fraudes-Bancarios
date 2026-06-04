from dash import html


def kpi_card(
    card_id: str,
    label: str,
    value: str,
    delta: str = "",
    icon: str = "●",
    bar_pct: int = 0,
    status: str = "normal",   # "normal" | "warn" | "danger"
) -> html.Div:
    """
    Retorna un Div con clases CSS que definen la severidad:
      • status-normal  → azul  (tranquilo)
      • status-warn    → ámbar (advertencia)
      • status-danger  → rojo  (anomalía/peligro)
    """
    # Clamp bar_pct entre 0 y 100
    bar_pct = max(0, min(100, bar_pct))

    return html.Div(
        id=card_id,
        className=f"card card-kpi status-{status}",
        children=[
            # Ícono decorativo de fondo
            html.Span(icon, className="card-kpi__icon"),

            # Etiqueta
            html.Div(label, className="card-kpi__label"),

            # Valor principal
            html.Div(value, className="card-kpi__value"),

            # Delta / comparación
            html.Div(delta, className="card-kpi__delta") if delta else None,

            # Barra de progreso inferior
            html.Div(
                className="card-kpi__bar",
                children=[
                    html.Div(
                        className="card-kpi__bar-fill",
                        style={"width": f"{bar_pct}%"},
                    )
                ],
            ),
        ],
    )

"""
components/content_card.py
─────────────────────────────────────────────────────────────
Componente: Content Card
Plantilla reutilizable para tarjetas de gráficas / tablas / contenido.
Acepta cualquier componente Dash como hijo (gráfica Plotly, tabla, etc.)

Uso:
    from components.content_card import content_card
    import plotly.graph_objects as go
    from dash import dcc

    fig = go.Figure(...)   # tu gráfica

    content_card(
        card_id  = "card-serie-temporal",
        title    = "Serie temporal — Tráfico de red",
        badge    = "NORMAL",                    # texto del badge
        badge_status = "normal",               # "normal" | "warn" | "danger"
        children = dcc.Graph(figure=fig, ...),  # contenido real
        wide     = True,                        # True → class card--wide (50%)
        status   = "normal",                    # borde/glow de la card
    )
"""

from dash import html


def content_card(
    card_id: str,
    title: str,
    children=None,
    badge: str = "",
    badge_status: str = "normal",   # "normal" | "warn" | "danger"
    wide: bool = False,
    status: str = "normal",         # "normal" | "warn" | "danger"
) -> html.Div:
    """
    Retorna una card con:
      • Encabezado (título + badge opcional)
      • Cuerpo flexible para cualquier contenido Dash
      • Modificador --wide para la columna ancha del grid asimétrico
    """
    card_classes = f"card card-content status-{status}"
    if wide:
        card_classes += " card--wide"

    header_children = [
        html.Span(title, className="card-content__title"),
    ]

    if badge:
        header_children.append(
            html.Span(
                [html.Span("●", style={"fontSize": "8px"}), f" {badge}"],
                className=f"badge badge--{badge_status}",
            )
        )

    return html.Div(
        id=card_id,
        className=card_classes,
        children=[
            # ── Encabezado ────────────────────────────────────
            html.Div(
                className="card-content__header",
                children=header_children,
            ),
            # ── Cuerpo ────────────────────────────────────────
            html.Div(
                className="card-content__body",
                children=children or html.Span(
                    "[ componente aquí ]",
                    style={"fontFamily": "var(--font-display)", "fontSize": "11px"},
                ),
            ),
        ],
    )