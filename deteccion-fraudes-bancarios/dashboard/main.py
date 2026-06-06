from src.app import app
from src.layout import serve_layout
from src.callbacks import register_callbacks

app.layout = serve_layout()

register_callbacks()

if __name__ == '__main__':
    app.run(debug=True)