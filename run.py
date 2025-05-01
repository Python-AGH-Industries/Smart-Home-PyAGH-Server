from app import create_app
from app.components.flask_app import app

app = create_app()

if __name__ == '__main__':
    app.run(debug = False)
