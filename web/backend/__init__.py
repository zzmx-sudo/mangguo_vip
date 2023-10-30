__all__ = [
    "create_app"
]

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from utils.commons import ReConverter
from . config import Config

# 数据库
db = SQLAlchemy()
from web.backend import models

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    Migrate(app, db)

    # 配置转换器和路由
    app.url_map.converters["re"] = ReConverter
    from api_1_0 import api
    app.register_blueprint(api, url_prefix="/api")

    from web_html import html
    app.register_blueprint(html, url_prefix="")

    return app
