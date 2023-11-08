from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import settings

if settings.SYSTEM == "Darwin":
    import pymysql
    pymysql.install_as_MySQLdb()

engine = create_engine(
    settings.MYSQL_URL,
    echo=True,
    pool_size=5,
    pool_recycle=60*30
)

Base = declarative_base()

class ExchangeModel(Base):

    __tablename__ = "tb_exchange_record"

    id = Column(Integer, primary_key=True)
    telephone = Column(String(11), unique=True, nullable=False)
    sms_code = Column(String(10), nullable=True)
    exchange_code = Column(String(64), unique=True, nullable=False, index=True)
    status = Column(
        Enum(
            "DOING",  # 兑换中
            "FAIL",  # 兑换失败
            "SUCC"  # 兑换成功
        ),
        default="DOING", index=True)
    failed_msg = Column(String(256), nullable=True)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def createSession(cls):
        DbSession = sessionmaker(bind=engine)
        session = DbSession()

        return session

    @classmethod
    def updateStatus(cls, telephone, sms_code, exchange_code, status):
        """
        更新兑换状态, exchange_code不存在则创建且状态为兑换成功, 存在则修改状态为兑换成功
        """
        if status == "SUCC":
            failed_msg = ""
        else:
            failed_msg = status
            status = "FAIL"

        with cls.createSession() as conn:
            exchange = conn.query(cls).filter(cls.exchange_code == exchange_code).all()
            if exchange:
                exchange.update({"status": status, "failed_msg": failed_msg})
            else:
                exchange = cls(
                    telephone=telephone, sms_code=sms_code, exchange_code=exchange_code,
                    status=status, failed_msg=failed_msg
                )
                conn.add(exchange)

            conn.commit()