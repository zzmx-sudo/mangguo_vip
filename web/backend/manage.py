import api_1_0
from utils.commons import ReConverter
from flask import Flask

app = Flask(__name__)

app.register_blueprint(api_1_0.api, url_prefix="")
app.url_map.converters["re"] = ReConverter


if __name__ == '__main__':
    app.run(debug=True)
