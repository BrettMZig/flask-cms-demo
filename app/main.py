from flask import Flask
from flaskext.markdown import Markdown
from .config import Config

# Flask app
app = Flask(__name__)
app.config.from_object(Config)

# add Markdown Capability
md = Markdown(app)


@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)


app.debug = True
if(app.debug):
    from werkzeug.debug import DebuggedApplication
    app.swgi_app = DebuggedApplication(app.wsgi_app, True)

