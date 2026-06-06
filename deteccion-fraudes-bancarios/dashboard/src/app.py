import os
import dash

# Apunta a la carpeta assets/ en la raíz del proyecto (un nivel arriba de src/)
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ASSETS = os.path.join(_ROOT, "assets")

external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3/tabler-icons.min.css",
]

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
    assets_folder=_ASSETS,          # ← ruta absoluta a assets/
    title="Anomaly Watch — Panel de Control",
)

server = app.server