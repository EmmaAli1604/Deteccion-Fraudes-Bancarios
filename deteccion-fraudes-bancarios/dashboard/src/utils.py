"""
src/utils.py
──────────────────────────────────────────────────────────────
Componentes reutilizables: kpi_card  y  content_card.
Requieren el CSS en src/assets/styles.css (Dash lo carga solo).
"""

from dash import html


# ── KPI Card ──────────────────────────────────────────────────

_DELTA_ICON = {
    "up":   "ti-trending-up",
    "down": "ti-trending-down",
}


def kpi_card(
    card_id: str,
    label: str,
    value: str,
    delta: str = "",
    delta_dir: str | None = None,   # "up" | "down" | None
    icon: str = "ti-circle",        # clase Tabler, p.ej. "ti-cpu"
    bar_pct: int = 0,
    status: str = "normal",         # "normal" | "warn" | "danger"
) -> html.Div:
    """
    Tarjeta KPI con franja de color lateral, ícono Tabler,
    valor principal, delta con tendencia y barra de progreso.

    Estados:
        normal  → azul
        warn    → ámbar
        danger  → rojo
    """
    bar_pct = max(0, min(100, bar_pct))

    delta_items = []
    if delta_dir in _DELTA_ICON:
        delta_items.append(
            html.I(
                className=f"ti {_DELTA_ICON[delta_dir]}",
                **{"aria-hidden": "true"},
            )
        )
    delta_items.append(delta)

    delta_cls = "kpi__delta"
    if delta_dir == "up":
        delta_cls += " delta--up"
    elif delta_dir == "down":
        delta_cls += " delta--down"

    return html.Div(
        id=card_id,
        className=f"kpi kpi--{status}",
        children=[
            html.Div(className="kpi__accent"),
            html.I(className=f"ti {icon} kpi__icon", **{"aria-hidden": "true"}),
            html.Div(label, className="kpi__label"),
            html.Div(value, className="kpi__value"),
            html.Div(delta_items, className=delta_cls) if delta else None,
            html.Div(
                className="kpi__bar",
                children=[
                    html.Div(
                        className="kpi__bar-fill",
                        style={"width": f"{bar_pct}%"},
                    )
                ],
            ),
        ],
    )


# ── Content Card ──────────────────────────────────────────────

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
    Tarjeta de contenido con encabezado (título + badge) y cuerpo libre.
    Acepta cualquier componente Dash como hijo.

    Modificadores:
        wide=True  → ocupa todo el ancho del grid (grid-column: 1 / -1)
        status     → controla el color del borde superior
    """
    card_cls = f"cc cc--{status}"
    if wide:
        card_cls += " card--wide"

    header = [html.Span(title, className="cc__title")]

    if badge:
        header.append(
            html.Span(
                [html.Span(className="badge__dot"), f"\u00a0{badge}"],
                className=f"badge badge--{badge_status}",
            )
        )

    return html.Div(
        id=card_id,
        className=card_cls,
        children=[
            html.Div(className="cc__header", children=header),
            html.Div(
                className="cc__body",
                children=children or html.Span(
                    "[ componente aquí ]",
                    style={"fontSize": "12px", "color": "var(--color-text-tertiary)"},
                ),
            ),
        ],
    )