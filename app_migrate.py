from app import app, db
from flask_migrate import Migrate

migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run("0.0.0.0")
