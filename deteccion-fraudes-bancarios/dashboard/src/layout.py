from __future__ import annotations

import pathlib
import time

import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html

from .utils import content_card, kpi_card

# ══════════════════════════════════════════════════════════════
# 1. CARGA DE DATOS
# ══════════════════════════════════════════════════════════════

_HERE    = pathlib.Path(__file__).resolve().parent
_ROOT    = _HERE.parent
_PARQUET = _ROOT.parent / "data/01_raw/transacciones_bancarias_raw.parquet"
_CSV     = _ROOT.parent / "data/01_raw/PS_20174392719_1491204439457_log.csv"

_RENAME = {
    "nameOrig": "nameOrig", "nameorig": "nameOrig",
    "nameDest": "nameDest", "namedest": "nameDest",
    "oldbalanceOrg":  "oldbalanceOrg",  "oldbalanceorg":  "oldbalanceOrg",
    "newbalanceOrig": "newbalanceOrig",  "newbalanceorig": "newbalanceOrig",
    "oldbalanceDest": "oldbalanceDest",  "oldbalancedest": "oldbalanceDest",
    "newbalanceDest": "newbalanceDest",  "newbalancedest": "newbalanceDest",
    "isFraud":        "isFraud",         "isfraud":        "isFraud",
    "isFlaggedFraud": "isFlaggedFraud",  "isflaggedfraud": "isFlaggedFraud",
}


def _load_data() -> pd.DataFrame:
    t0 = time.time()

    if _PARQUET.exists():
        print(f"\n[layout] ⚡ Leyendo Parquet...")
        df = pd.read_parquet(_PARQUET)
    elif _CSV.exists():
        print(f"\n[layout] 📂 Leyendo CSV (será lento, genera el parquet primero)...")
        df = pd.read_csv(
            _CSV,
            dtype={
                "step": "int32", "type": "category",
                "amount": "float32", "oldbalanceOrg": "float32",
                "newbalanceOrig": "float32", "oldbalanceDest": "float32",
                "newbalanceDest": "float32", "isFraud": "int8",
                "isFlaggedFraud": "int8",
            },
            engine="c",
        )
    else:
        raise FileNotFoundError("No se encontró ni Parquet ni CSV del dataset.")

    df.columns = df.columns.str.strip()
    df = df.rename(columns={c: _RENAME.get(c, c) for c in df.columns})
    print(f"[layout] ✅ {len(df):,} filas en {time.time()-t0:.1f}s\n")
    return df


try:
    _df: pd.DataFrame = _load_data()
    _DATA_OK = True
except Exception as _err:
    print(f"[layout] ❌ {_err}")
    _df = pd.DataFrame()
    _DATA_OK = False


# ══════════════════════════════════════════════════════════════
# 2. CONFIGURACIÓN GLOBAL DE GRÁFICAS
# ══════════════════════════════════════════════════════════════

PLOT_CONFIG = {"displayModeBar": False, "responsive": True}

_BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="'DM Mono', monospace", color="#7fa8cc", size=11),
    margin=dict(l=40, r=16, t=16, b=40),
    showlegend=False,
)

FILTRO_OPTIONS = [
    {"label": "Opción A — Transacciones normales",    "value": "A"},
    {"label": "Opción B — Transacciones sospechosas", "value": "B"},
]


def _graph(fig: go.Figure, height: int = 220) -> dcc.Graph:
    return dcc.Graph(
        figure=fig,
        config=PLOT_CONFIG,
        style={"height": f"{height}px", "width": "100%"},
    )


# ══════════════════════════════════════════════════════════════
# 3. CÁLCULO DE COMPONENTES — SE EJECUTA UNA SOLA VEZ AL IMPORTAR
# ══════════════════════════════════════════════════════════════

def _build_components(df: pd.DataFrame) -> dict:
    """
    Calcula todos los componentes costosos una sola vez.
    serve_layout() los reutiliza en cada request sin recalcular.
    """
    print("[layout] 🔧 Precalculando componentes del dashboard...")
    t0 = time.time()

    if df.empty:
        empty = html.Span("Sin datos", className="no-data")
        return {k: empty for k in [
            "kpis", "top10_txn", "top10_orig", "top10_dest",
            "fig_bar_tipo", "fig_scatter", "null_values",
            "filas", "columnas",
        ]}

    # ── KPIs ────────────────────────────────────────────────
    total      = len(df)
    pct_fraude = df["isFraud"].mean() * 100
    monto_mod  = df["amount"].mode().iloc[0]
    std_monto  = df["amount"].std()

    amounts = df["amount"].sort_values().values
    n = len(amounts)
    gini = float(
        (2 * (amounts * range(1, n + 1)).sum() / (n * amounts.sum())) - (n + 1) / n
    )

    kpis = {
        "total":       f"{total:,}",
        "pct_fraude":  f"{pct_fraude:.4f} %",
        "monto_comun": f"$ {monto_mod:,.2f}",
        "gini":        f"{gini:.4f}",
        "std_monto":   f"$ {std_monto:,.2f}",
    }

    # ── Top 10 transacciones ─────────────────────────────────
    top_txn = (
        df.nlargest(10, "amount")
          [["step", "type", "nameOrig", "nameDest", "amount", "isFraud"]]
          .copy()
    )
    top_txn["amount"]  = top_txn["amount"].apply(lambda v: f"$ {v:,.2f}")
    top_txn["isFraud"] = top_txn["isFraud"].apply(lambda v: "⚠ Fraude" if v else "✓ OK")
    c_top_txn = _tabla(
        ["Paso", "Tipo", "Origen", "Destino", "Monto", "Estado"],
        top_txn.values.tolist(),
    )

    # ── Top 10 cuentas origen ────────────────────────────────
    top_orig = (
        df.groupby("nameOrig")["amount"].sum()
          .nlargest(10).reset_index()
    )
    top_orig["amount"] = top_orig["amount"].apply(lambda v: f"$ {v:,.2f}")
    c_top_orig = _tabla(
        ["Cuenta origen", "Monto total acumulado"],
        top_orig.values.tolist(),
    )

    # ── Top 10 destinatarios ─────────────────────────────────
    top_dest = df["nameDest"].value_counts().head(10).reset_index()
    top_dest.columns = ["nameDest", "count"]
    top_dest["count"] = top_dest["count"].apply(lambda v: f"{v:,}")
    c_top_dest = _tabla(
        ["Cuenta destino", "Nº transacciones"],
        top_dest.values.tolist(),
    )

    # ── Bar chart por tipo ───────────────────────────────────
    counts = df["type"].value_counts().reset_index()
    counts.columns = ["type", "count"]
    colors = ["#E24B4A" if t in ("TRANSFER", "CASH_OUT") else "#378ADD"
              for t in counts["type"]]

    fig_bar = go.Figure(
        go.Bar(
            x=counts["type"], y=counts["count"],
            marker_color=colors, marker_line_width=0,
            text=counts["count"].apply(lambda v: f"{v:,}"),
            textposition="outside",
            textfont=dict(size=10, color="#7fa8cc"),
        ),
        layout={
            **_BASE_LAYOUT,
            "xaxis": dict(showgrid=False, zeroline=False),
            "yaxis": dict(showgrid=True, gridcolor="rgba(55,138,221,0.08)",
                          zeroline=False),
        },
    )

    # ── Scatter monto vs saldo — máx 2000 puntos ─────────────
    s = df.sample(min(2_000, len(df)), random_state=42)
    fig_scatter = go.Figure(
        go.Scatter(
            x=s["amount"].round(0).tolist(),          # round → JSON más liviano
            y=s["newbalanceOrig"].round(0).tolist(),
            mode="markers",
            marker=dict(
                color=["#E24B4A" if f else "#378ADD" for f in s["isFraud"]],
                size=4, opacity=0.55,
            ),
            hovertemplate="Monto: $%{x:,.0f}<br>Saldo: $%{y:,.0f}<extra></extra>",
        ),
        layout={
            **_BASE_LAYOUT,
            "xaxis": dict(title="Monto", showgrid=True,
                          gridcolor="rgba(55,138,221,0.08)", zeroline=False),
            "yaxis": dict(title="Nuevo saldo origen", showgrid=True,
                          gridcolor="rgba(55,138,221,0.08)", zeroline=False),
        },
    )

    # ── Valores nulos ────────────────────────────────────────
    nulls = df.isnull().sum().reset_index()
    nulls.columns = ["Columna", "Nulos"]
    c_nulls = _tabla(
        ["Columna", "Valores nulos"],
        nulls.values.tolist(),
    )

    print(f"[layout] ✅ Componentes listos en {time.time()-t0:.1f}s\n")

    return {
        "kpis":        kpis,
        "top10_txn":   c_top_txn,
        "top10_orig":  c_top_orig,
        "top10_dest":  c_top_dest,
        "fig_bar_tipo": fig_bar,
        "fig_scatter":  fig_scatter,
        "null_values":  c_nulls,
        "filas":        f"{len(df):,}",
        "columnas":     str(len(df.columns)),
    }


def _tabla(headers: list[str], rows: list[list]) -> html.Table:
    return html.Table(
        className="data-table",
        children=[
            html.Thead(html.Tr([html.Th(h) for h in headers])),
            html.Tbody([
                html.Tr([html.Td(str(cell)) for cell in row])
                for row in rows
            ]),
        ],
    )


# ── Precalculo al importar ───────────────────────────────────
_C = _build_components(_df)


# ══════════════════════════════════════════════════════════════
# 4. SERVE_LAYOUT — ensamblado rápido con componentes ya listos
# ══════════════════════════════════════════════════════════════

def serve_layout() -> html.Div:
    kpis = _C["kpis"] if isinstance(_C["kpis"], dict) else {}

    # ── HEADER ──────────────────────────────────────────────
    header = html.Header(
        className="dash-header",
        children=[
            html.Div(className="dash-header__left", children=[
                html.Div("Análisis Exploratorio de Transacciones",
                         className="dash-header__title"),
                html.Div(
                    f"FILAS: {_C['filas']}  ·  COLUMNAS: {_C['columnas']}"
                    if _DATA_OK else "⚠ Dataset no disponible",
                    className="dash-header__subtitle",
                ),
            ]),
            html.Div(className="dash-header__right", children=[
                html.Span(
                    [html.Span(className="live-dot"), "EN VIVO"],
                    className="badge-live",
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
                    kpi_card(card_id="kpi-1", label="Total de transacciones",
                             value=kpis.get("total", "—"),
                             icon="ti-receipt",    bar_pct=100, status="normal"),
                    kpi_card(card_id="kpi-2", label="Porcentaje de fraudes",
                             value=kpis.get("pct_fraude", "—"),
                             icon="ti-alert-triangle", bar_pct=12, status="danger"),
                    kpi_card(card_id="kpi-3", label="Monto más común",
                             value=kpis.get("monto_comun", "—"),
                             icon="ti-coin",       bar_pct=60,  status="normal"),
                    kpi_card(card_id="kpi-4", label="Índice de Gini (monto)",
                             value=kpis.get("gini", "—"),
                             icon="ti-chart-bar",  bar_pct=79,  status="warn"),
                    kpi_card(card_id="kpi-5", label="Desviación estándar",
                             value=kpis.get("std_monto", "—"),
                             icon="ti-wave-sine",  bar_pct=55,  status="normal"),
                ],
            ),
        ],
    )

    # ── FILA 2: Tablas exploratorias ────────────────────────
    filtro_row = html.Section(
        className="dash-section",
        children=[
            html.P("Exploración de transacciones", className="section-label"),
            html.Div(
                className="asymmetric-grid",
                children=[
                    content_card(
                        card_id="card-top10-txn",
                        title="Top 10 transacciones por monto",
                        badge="Datos reales", badge_status="normal",
                        status="normal", wide=True,
                        children=_C["top10_txn"],
                    ),
                    content_card(
                        card_id="card-top10-orig",
                        title="Top 10 cuentas origen",
                        badge="Agregado", badge_status="normal", status="normal",
                        children=_C["top10_orig"],
                    ),
                    content_card(
                        card_id="card-top10-dest",
                        title="Top 10 destinatarios frecuentes",
                        badge="Frecuencia", badge_status="warn", status="warn",
                        children=_C["top10_dest"],
                    ),
                ],
            ),
        ],
    )

    # ── FILA 3: Gráficas ────────────────────────────────────
    row3 = html.Section(
        className="dash-section",
        children=[
            html.P("Distribución & dispersión", className="section-label"),
            html.Div(
                className="asymmetric-grid",
                children=[
                    content_card(
                        card_id="card-bar-tipo",
                        title="Transacciones por tipo",
                        badge="Riesgo en rojo", badge_status="danger",
                        status="danger", wide=True,
                        children=_graph(_C["fig_bar_tipo"], height=260),
                    ),
                    content_card(
                        card_id="card-scatter",
                        title="Dispersión: monto vs saldo origen",
                        badge="Muestra 2 000 pts", badge_status="warn", status="warn",
                        children=_graph(_C["fig_scatter"], height=260),
                    ),
                    content_card(
                        card_id="card-nulls",
                        title="Valores nulos por columna",
                        badge="Calidad de datos", badge_status="normal", status="normal",
                        children=_C["null_values"],
                    ),
                ],
            ),
        ],
    )

    # ── FOOTER ───────────────────────────────────────────────
    footer = html.Footer(
        className="dash-footer",
        children=[
            html.Span("Fuente del dataset: ", className="dash-footer__label"),
            html.A(
                "Fraud Detection Dynamics — Financial Transactions (Kaggle)",
                href="https://www.kaggle.com/datasets/rohit265/fraud-detection-dynamics-financial-transaction",
                target="_blank", rel="noopener noreferrer",
                className="dash-footer__link",
            ),
            html.Span(" · Extraído el 01/06/2026", className="dash-footer__date"),
        ],
    )

    return html.Div(
        className="dash-wrapper",
        children=[header, kpi_row, filtro_row, row3, footer],
    )