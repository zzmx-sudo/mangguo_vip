from datetime import datetime

from . import db

class BaseModel(object):

    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class ExchangeModel(BaseModel, db.Model):

    __tablename__ = "tb_exchange_record"

    id = db.Column(db.Integer, primary_key=True)
    telephone = db.Column(db.String(11), unique=True, nullable=False)
    sms_code = db.Column(db.String(6))
    exchange_code = db.Column(db.String(8), unique=True, nullable=False)
    status = db.Column(
        db.Enum(
            "DOING",    # 兑换中
            "FAIL",     # 兑换失败
            "SUCC"      # 兑换成功
        ),
    default="DOING", index=True)