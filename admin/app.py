from src.web import create_app
from flask_cors import CORS

app = create_app()


if __name__ == "main":
    app.run()