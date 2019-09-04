from flask import Flask
from .config import Config

# Flask app
app = Flask(__name__)
app.config.from_object(Config)

app.debug = True
if(app.debug):
    from werkzeug.debug import DebuggedApplication
    app.swgi_app = DebuggedApplication(app.wsgi_app, True)

