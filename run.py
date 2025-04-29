from app import create_app
from app.flask_app import app

app = create_app()

if __name__ == '__main__':
    app.run(debug = False)
