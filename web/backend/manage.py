from utils.commons import ReConverter
from flask import Flask

app = Flask(__name__)

app.url_map.converters["re"] = ReConverter

from api_1_0 import api
app.register_blueprint(api, url_prefix="/api")

from web_html import html
app.register_blueprint(html, url_prefix="")


if __name__ == '__main__':
    app.run(debug=True)
